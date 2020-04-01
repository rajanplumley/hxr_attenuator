from caproto.server import pvproperty, PVGroup
from caproto import ChannelType

class SystemGroup(PVGroup):
    """
    PV group for attenuator system-spanning information.
    """
    t_actual = pvproperty(value=0.1,
                          name='T_ACTUAL',
                          mock_record='ao',
                          upper_alarm_limit=1.0,
                          lower_alarm_limit=0.0,
                          doc='Actual transmission')

    t_high = pvproperty(value=0.1,
                        name='T_HIGH',
                        mock_record='ao',
                        upper_alarm_limit=1.0,
                        lower_alarm_limit=0.0,
                        doc='Desired transmission '
                        +'best achievable (high)')

    t_low = pvproperty(value=0.1,
                       name='T_LOW',
                       mock_record='ao',
                       upper_alarm_limit=1.0,
                       lower_alarm_limit=0.0,
                       doc='Desired transmission '
                       +'best achievable (low)')

    t_desired = pvproperty(value=0.1,
                           name='T_DESIRED',
                           mock_record='ao',
                           upper_alarm_limit=1.0,
                           lower_alarm_limit=0.0,
                           doc='Desired transmission')

    t_3omega = pvproperty(value=0.1,
                          name='T_3OMEGA',
                          mock_record='ao',
                          upper_alarm_limit=1.0,
                          lower_alarm_limit=0.0,
                          doc='Actual 3rd harmonic '
                          +'transmission')

    run = pvproperty(value='False',
                     name='RUN',
                     mock_record='bo',
                     enum_strings=['False', 'True'],
                     doc='Change transmission',
                     dtype=ChannelType.ENUM)

    running = pvproperty(value='False',
                         name='RUNNING',
                         mock_record='bo',
                         enum_strings=['False', 'True'],
                         doc='The system is running',
                         dtype=ChannelType.ENUM)

    mirror_in = pvproperty(value='False',
                           name='MIRROR_IN',
                           mock_record='bo',
                           enum_strings=['False', 'True'],
                           doc='The inspection mirror is in',
                           dtype=ChannelType.ENUM)

    def __init__(self, prefix, *, ioc, **kwargs):
        super().__init__(prefix, **kwargs)
        self.ioc = ioc
