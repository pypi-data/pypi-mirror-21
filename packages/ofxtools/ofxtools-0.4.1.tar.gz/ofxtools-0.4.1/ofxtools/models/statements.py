# vim: set fileencoding=utf-8
"""
Python object model for fundamental data aggregates such as transactions,
balances, and securities.
"""
# local imports
from ofxtools.Types import (
    String,
    Decimal,
    OneOf,
    DateTime,
)
from ofxtools.models import (
    Aggregate,
    CURRENCY_CODES,
)


class TRNRS(Aggregate):
    """ Base class for *TRNRS (not in OFX spec) """
    trnuid = String(36, required=True)
    curdef = OneOf(*CURRENCY_CODES, required=True)
    mktginfo = String(360)

    _rsTag = None
    _acctTag = None
    _tranList = None

    @classmethod
    def _preflatten(cls, elem):
        """ """
        # Don't call super() - start with a clean sheet
        # For statements we want to interpret cls._subaggregates
        # differently than Aggregate._preflatten()
        subaggs = {}

        status = elem.find('STATUS')
        subaggs['STATUS'] = status
        elem.remove(status)

        stmtrs = elem.find(cls._rsTag)

        acctfrom = stmtrs.find(cls._acctTag)
        if acctfrom is None:
            msg = "Can't find {}".format(cls._acctTag)
            raise ValueError(msg)
        subaggs[cls._acctTag] = acctfrom
        stmtrs.remove(acctfrom)

        tranlist = stmtrs.find(cls._tranList)
        if tranlist is not None:
            subaggs[cls._tranList] = tranlist
            stmtrs.remove(tranlist)

        # N.B. as opposed to Aggregate._preflatten(), TRNRS._preflatten()
        # searches for _subaggregates in the *RS child, not the *TRNRS itself.
        for tag in cls._subaggregates:
            subagg = stmtrs.find(tag)
            if subagg is not None:
                stmtrs.remove(subagg)
                subaggs[tag] = subagg

        # Unsupported subaggregates
        for tag in cls._unsupported:
            child = stmtrs.find(tag)
            if child is not None:
                stmtrs.remove(child)

        return subaggs

    # Human-friendly attribute aliases
    @property
    def currency(self):
        return self.curdef

    @property
    def account(self):
        attr = getattr(self, self._acctTag.lower())
        return attr

    @property
    def transactions(self):
        attr = getattr(self, self._tranList.lower())
        return attr


class STMTTRNRS(TRNRS):
    """ OFX section 11.4.2.2 """
    cashadvbalamt = Decimal()
    intrate = Decimal()

    _subaggregates = ('LEDGERBAL', 'AVAILBAL', 'BALLIST',)

    _rsTag = 'STMTRS'
    _acctTag = 'BANKACCTFROM'
    _tranList = 'BANKTRANLIST'
    _unsupported = ('BANKTRANLISTP',)

    @classmethod
    def _preflatten(cls, elem):
        """
        LEDGERBAL is a required subaggregate for STMTTRNRS, CCSTMTTRNS
        """
        subaggs = super(STMTTRNRS, cls)._preflatten(elem)
        if 'LEDGERBAL' not in subaggs:
            msg = "Can't find {}".format('LEDGERBAL')
            raise ValueError(msg)

        return subaggs


class CCSTMTTRNRS(STMTTRNRS):
    """ OFX section 11.4.3.2 """
    intrate = None
    intratepurch = Decimal()
    intratecash = Decimal()
    intratexfer = Decimal()
    rewardname = String(32)
    rewardbal = Decimal()
    rewardearned = Decimal()

    _subaggregates = ('LEDGERBAL', 'AVAILBAL', 'BALLIST',)

    _rsTag = 'CCSTMTRS'
    _acctTag = 'CCACCTFROM'
    _unsupported = ('BANKTRANLISTP',)

    @staticmethod
    def _groom(elem):
        """
        Rename NAME (from REWARDINFO) to REWARDNAME.
        """
        super(CCSTMTTRNRS, CCSTMTTRNRS)._groom(elem)

        yld = elem.find('./*/REWARDINFO/NAME')
        if yld is not None:
            yld.tag = 'REWARDNAME'


class INVSTMTTRNRS(TRNRS):
    """ OFX section 13.9.2.1 """
    dtasof = DateTime(required=True)
    clientcookie = String(32)

    _subaggregates = ('INVPOSLIST', 'INVBAL', 'INVOOLIST', 'INV401KBAL')

    _rsTag = 'INVSTMTRS'
    _acctTag = 'INVACCTFROM'
    _tranList = 'INVTRANLIST'
    _unsupported = ('INV401K',)

    @classmethod
    def _preflatten(cls, elem):
        """ """
        subaggs = super(INVSTMTTRNRS, cls)._preflatten(elem)

        # Find OFXEXTENSION directly in INVSTMTTRNRS, not INVSTMTRS
        ofxextension = elem.find('OFXEXTENSION')
        if ofxextension:
            subaggs['OFXEXTENSION'] = ofxextension
            elem.remove(ofxextension)

        return subaggs

    # Human-friendly attribute aliases
    @property
    def datetime(self):
        return self.dtasof

    @property
    def positions(self):
        return self.invposlist
