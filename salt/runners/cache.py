'''
Return cached data from minions
'''
# Import python libs
import logging

# Import salt libs
import salt.log
import salt.utils.master
import salt.output
import salt.payload
from salt._compat import string_types

log = logging.getLogger(__name__)

deprecation_warning = ("The 'minion' arg will be removed from "
                    "cache.py runner. Specify minion with 'tgt' arg!")

def grains(tgt=None, expr_form='glob', **kwargs):
    '''
    Return cached grains of the targeted minions
    '''
    deprecated_minion = kwargs.get('minion', None)
    if tgt is None and deprecated_minion is None:
        log.warn("DEPRECATION WARNING: {0}".format(deprecation_warning))
        tgt = '*' # targat all minions for backward compatibility
    elif tgt is None and isinstance(deprecated_minion, string_types):
        log.warn("DEPRECATION WARNING: {0}".format(deprecation_warning))
        tgt = deprecated_minion
    elif tgt is None:
        return {}
    pillar_util = salt.utils.master.MasterPillarUtil(tgt, expr_form,
                                                use_cached_grains=True,
                                                grains_fallback=False,
                                                opts=__opts__)
    cached_grains = pillar_util.get_minion_grains()
    salt.output.display_output(cached_grains, None, __opts__)
    return cached_grains


def pillar(tgt=None, expr_form='glob', **kwargs):
    '''
    Return cached pillars of the targeted minions
    '''
    deprecated_minion = kwargs.get('minion', None)
    if tgt is None and deprecated_minion is None:
        log.warn("DEPRECATION WARNING: {0}".format(deprecation_warning))
        tgt = '*' # targat all minions for backward compatibility
    elif tgt is None and isinstance(deprecated_minion, string_types):
        log.warn("DEPRECATION WARNING: {0}".format(deprecation_warning))
        tgt = deprecated_minion
    elif tgt is None:
        return {}
    pillar_util = salt.utils.master.MasterPillarUtil(tgt, expr_form,
                                                use_cached_grains=True,
                                                grains_fallback=False,
                                                use_cached_pillar=True,
                                                pillar_fallback=False,
                                                opts=__opts__)
    cached_pillar = pillar_util.get_minion_pillar()
    salt.output.display_output(cached_pillar, None, __opts__)
    return cached_pillar
