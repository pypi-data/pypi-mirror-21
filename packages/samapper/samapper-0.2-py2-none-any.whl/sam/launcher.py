import sys
import os
sys.path.append(os.path.dirname(__file__))  # this could be executed from any directory
import getopt
from sam import constants
import multiprocessing

application = None

# targets:
#   webserver
#     --target=webserver
#   wsgi webserver
#     --target=webserver --wsgi
#   aggregator
#     --target=aggregator
#   wsgi aggregator
#     --target=aggregator --wsgi
#   collector
#     --target=collector
#   localmode combo
#     --local --scanner=tcpdump

# suggested demo invocation:
# sudo tcpdump -i any -f --immediate-mode -l -n -Q inout -tt | python launcher.py --local --whois --format=tcpdump


def main(argv=None):
    if argv == None:
        argv = sys.argv

    kwargs, args = getopt.getopt(argv[1:], '', ['format=', 'port=', 'target=', 'local', 'whois', 'wsgi'])

    defaults = {
        'format': 'tcpdump',
        'port': None,
        'target': 'webserver',
        'local': False,
        'whois': False,
        'wsgi': False,
    }
    valid_formats = ['tcpdump', 'none']
    valid_targets = ['aggregator', 'collector', 'webserver']

    parsed_args = defaults.copy()
    for key, val in kwargs:
        if key == '--local':
            parsed_args['local'] = True
        if key == '--wsgi':
            parsed_args['wsgi'] = True
        if key == '--whois':
            parsed_args['whois'] = True
        if key == '--format':
            parsed_args['format'] = val
        if key == '--target':
            parsed_args['target'] = val
        if key == '--port':
            parsed_args['port'] = val

    if parsed_args['format'] not in valid_formats:
        print("Invalid format")
        sys.exit(1)
    if parsed_args['target'] not in valid_targets:
        print("Invalid target")
        sys.exit(1)

    if parsed_args['whois']:
        constants.use_whois = True

    if parsed_args['local']:
        launch_localmode(parsed_args)
    elif parsed_args['target'] == 'webserver':
        launch_webserver(parsed_args)
    elif parsed_args['target'] == 'collector':
        launch_collector(parsed_args)
    elif parsed_args['target'] == 'aggregator':
        launch_aggregator(parsed_args)
    else:
        print("Error determining what to launch.")


def launch_webserver(args):
    import server_webserver
    if args['wsgi']:
        print('launching wsgi webserver')
        global application
        application = server_webserver.start_wsgi()
    else:
        port = args['port']
        if port is None:
            port = constants.webserver['listen_port']
        print('launching dev webserver on {}'.format(port))
        server_webserver.start_server(port=port)
        print('webserver shut down.')


def launch_collector(args):
    import server_collector
    port = args.get('port', None)
    if port is None:
        port = constants.collector['listen_port']
    print('launching collector on {}'.format(args['port']))
    collector = server_collector.Collector()
    collector.run(port=args['port'], format=args['format'])
    print('collector shut down.')


def launch_aggregator(args):
    import server_aggregator
    if args['wsgi']:
        print("launching wsgi aggregator")
        global application
        application = server_aggregator.start_wsgi()
    else:
        port = args.get('port', None)
        if port is None:
            port = constants.aggregator['listen_port']
        print('launching dev aggregator on {}'.format(port))
        server_aggregator.start_server(port=port)
        print('aggregator shut down.')


def create_local_settings(db, sub):
    # create 1 key if none exist
    import models.settings
    import models.datasources
    import models.livekeys

    m_set = models.settings.Settings(db, {}, sub)
    ds_id = m_set['datasource']
    m_livekeys = models.livekeys.LiveKeys(db, sub)

    # set useful settings for local viewing.
    m_ds = models.datasources.Datasources(db, {}, sub)
    m_ds.set(ds_id, flat='1', ar_active='1', ar_interval=30)

    # create key for uploading securely
    keys = m_livekeys.read()
    if len(keys) == 0:
        m_livekeys.create(ds_id)

    keys = m_livekeys.read()
    key = keys[0]['access_key']
    constants.collector['upload_key'] = key
    return key


def check_database():
    import integrity
    # Validate the database format
    if not integrity.check_and_fix_integrity():
        exit(1)


def launch_whois_service(db, sub):
    import models.nodes
    whois = models.nodes.WhoisService(db, sub)
    whois.start()
    return whois


def launch_localmode(args):
    import server_collector

    # enable local mode
    constants.enable_local_mode()
    import common
    db = common.db_quiet
    sub_id = constants.demo['id']
    check_database()
    access_key = create_local_settings(db, sub_id)

    # launch aggregator process
    aggArgs = args.copy()
    aggArgs.pop('port')
    p_aggregator = multiprocessing.Process(target=launch_aggregator, args=(aggArgs,))
    p_aggregator.start()

    # launch collector process
    #    pipe stdin into the collector
    def spawn_coll(stdin):
        collector = server_collector.Collector()
        collector.run_streamreader(stdin, format=args['format'], access_key=access_key)
    newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
    try:
        p_collector = multiprocessing.Process(target=spawn_coll, args=(newstdin,))
        p_collector.start()
    finally:
        newstdin.close()  # close in the parent

    # launch whois service (if requested)
    if args['whois']:
        print("Starting whois service")
        import models.nodes
        whois_thread = models.nodes.WhoisService(db, sub_id)
        whois_thread.start()
    else:
        whois_thread = None

    # launch webserver locally.
    launch_webserver(args)

    # pressing ctrl-C sends SIGINT to all child processes. The shutdown order is not guaranteed.
    print("joining collector")
    p_collector.join()
    print("collector joined")

    print("joining aggregator")
    p_aggregator.join()
    print("aggregator joined")

    if args['whois']:
        print('joining whois')
        if whois_thread and whois_thread.is_alive():
            whois_thread.shutdown()
            whois_thread.join()
        print('whois joined')


if __name__ == '__main__':
    main(sys.argv)