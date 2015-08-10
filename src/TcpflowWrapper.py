import re
import Utilities as utils

if utils.runs_on() == 'debian':
    from bs4 import BeautifulSoup as Soup
elif utils.runs_on() == 'arch':
    from BeautifulSoup import BeautifulSoup as Soup

class TcpflowWrapper():

    def __init__(self, verbose):
        self.verbose = verbose

    def as_main_process(self, interface, output_dir):
        tcpflow = 'tcpflow -i ' + interface + ' -e http -o ' + output_dir
        try:
            proc = utils.start_subprocess(tcpflow, self.verbose)

            while proc.poll() is None:
                if self.verbose: print proc.stdout.readline()

        except KeyboardInterrupt:
            print 'Got Keyboard interrupt. Stopping..'

    def get_ips_from_filepath(self, filepath, exclude):
        ips = re.findall(utils.ipv4s_regex(leading_zeros=True), filepath)

        if len(ips) != 2:
            raise ValueError('The %s IP src/dst were not found in its filename.' % filepath)

        src_ip = utils.remove_ipv4_leading_zeros(ips[0])
        dst_ip = utils.remove_ipv4_leading_zeros(ips[1])
        ips = [src_ip, dst_ip]
        
        if (src_ip or dst_ip) in exclude: return ips, True
        return ips, False

    def get_macs_from_report(self, filename, report_path):
        ''' 
        XML report relevant structure:
            fileobject
                filename            <--     root_filename
                filesize
                tcpflow             <--     mac addresses and more
            byte_runs
                byte_run
                filename            <--     root_filename--HTTPBODY-#-?.?
                filesize
        '''
        root_filename = filename[0:filename.rfind('-HTTPBODY-')]
        smac = None
        dmac = None

        with open(report_path) as report:
            handler = report.read()
            soup = Soup(handler, 'lxml')

        for fileobject in soup.findAll('fileobject'):
            filename = fileobject.find('filename')

            if filename and root_filename in str(filename):
                tcpflow = fileobject.find('tcpflow')

                if tcpflow:
                        smac = str(tcpflow['mac_saddr'])
                        dmac = str(tcpflow['mac_daddr'])
        macs = [smac, dmac]

        if len(macs) != 2: raise ValueError(
            'The packet MAC source or destination were not found in: %s.' % macs)
        
        return macs

