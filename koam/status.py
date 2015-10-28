#!/usr/bin/python

class KoamStatus:

    ORDER = [ 'Host', 'Date', 'OAM Begin', 'OAM End',
              'Merges Made', 'Total Merges',
              'OAM Last Cmd', 'emerge' ]
    
    @staticmethod
    def header():
        return (" " + KoamStatus.layout(dict(zip(KoamStatus.ORDER, KoamStatus.ORDER)))).replace("Merges Made Total Merges ", " Merges ")
    
    @staticmethod
    def layout(msg):
        KoamStatus.tidyup(msg)
        return "%(Host)-8s %(Date)-8s %(OAM Begin)9s %(OAM End)9s %(Merges Made)3s %(Total Merges)3s %(OAM Last Cmd)-25s %(emerge)s" % msg

    @staticmethod
    def removedate(date, timestamp):
        return timestamp[len(date)+1:] if timestamp.startswith(date) else timestamp
    
    @staticmethod
    def tidyup(msg):
        msg['OAM Begin'] = KoamStatus.removedate(msg['Date'], msg['OAM Begin'])
        msg['OAM End'] = KoamStatus.removedate(msg['Date'], msg['OAM End'])
        msg['OAM Last Cmd'] = msg['OAM Last Cmd'][:25]
        msg['emerge'] = msg['emerge'][:45]
        return msg

    @staticmethod
    def merges(msg):
        return (int(msg['Merges Made']), int(msg['Total Merges']))
