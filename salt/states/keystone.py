'''
Management of Keystone users.
==========================

:depends:   - keystoneclient Python module
:configuration: See :py:mod:`salt.modules.keystone` for setup instructions.

.. code-block:: yaml

    frank:
      keystone.user_present:
        - password: creds4you
        - email: test@example.com

'''

# Import python libs
import sys

# Import salt libs
import salt.utils


def __virtual__():
    '''
    Only load if the keystone module is in __salt__
    '''
    return 'keystone' if 'keystone.auth' in __salt__ else False


def user_present(name,
                 password,
                 email,
                 tenant=None,
                 enabled=True):
    '''
    Ensure that the keystone user is present with the specified properties.

    name
        The name of the user to manage

    password
        The password to use for this user

    email
        The email address for this user

    tenant
        The tenant for this user

    enabled
        Availability state for this user
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'User "{0}" is already present'.format(name)}

    # Validate tenant if set
    if tenant is not None:
        tenantdata = __salt__['keystone.tenant_get'](name=tenant)
        if 'Error' in tenantdata:
            ret['result'] = False
            ret['comment'] = 'Tenant "{0}" does not exist'.format(tenant)
            return ret
        tenant_id = tenantdata[tenant]['id']
    else:
        tenant_id = None

    # Check if user is already present
    user = __salt__['keystone.user_get'](name=name)
    if 'Error' not in user:
        if user[name]['email'] != email:
            __salt__['keystone.user_update'](name=name, email=email)
            ret['comment'] = 'User "{0}" has been updated'.format(name)
            ret['changes']['Email'] = 'Updated'
        if user[name]['enabled'] != enabled:
            __salt__['keystone.user_update'](name=name, enabled=enabled)
            ret['comment'] = 'User "{0}" has been updated'.format(name)
            ret['changes']['Enabled'] = 'Now {0}'.format(enabled)
        if user[name]['tenant_id'] != tenant_id:
            __salt__['keystone.user_update'](name=name, tenant=tenant)
            ret['comment'] = 'User "{0}" has been updated'.format(name)
            ret['changes']['Tenant'] = 'Added to "{0}" tenant'.format(tenant)
        if not __salt__['keystone.user_verify_password'](name=name,
                                                     password=password):
            __salt__['keystone.user_password_update'](name=name,
                                                      password=password)
            ret['comment'] = 'User "{0}" has been updated'.format(name)
            ret['changes']['Password'] = 'Updated'
    else:
        # Create that user!
        __salt__['keystone.user_create'](name=name,
                                         password=password,
                                         email=email,
                                         tenant_id=tenant_id,
                                         enabled=enabled)
        ret['comment'] = 'Keystone user {0} has been added'.format(name)
        ret['changes']['User'] = 'Created'

    return ret


def user_absent(name):
    '''
    Ensure that the keystone user is absent.

    name
        The name of the user that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'User "{0}" is already absent'.format(name)}

    # Check if user is present
    user = __salt__['keystone.user_get'](name=name)
    if 'Error' not in user:
        # Delete that user!
        __salt__['keystone.user_delete'](name=name)
        ret['comment'] = 'User "{0}" has been deleted'.format(name)
        ret['changes']['User'] = 'Deleted'

    return ret


def tenant_present(name, description=None, enabled=True):
    ''''
    Ensures that the keystone tenant exists

    name
        The name of the tenant to manage

    description
        The description to use for this tenant

    enabled
        Availability state for this tenant
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Tenant "{0}" already exists'.format(name)}

    # Check if user is already present
    tenant = __salt__['keystone.tenant_get'](name=name)
    
    if 'Error' not in tenant:
        if tenant[name]['description'] != description:
            __salt__['keystone.tenant_update'](name, description, enabled)
            comment = 'Tenant "{0}" has been updated'.format(name)
            ret['comment'] = comment
            ret['changes']['Description'] = 'Updated'
        if tenant[name]['enabled'] != enabled:
            __salt__['keystone.tenant_update'](name, description, enabled)
            comment = 'Tenant "{0}" has been updated'.format(name)
            ret['comment'] = comment
            ret['changes']['Enabled'] = 'Now {0}'.format(enabled)
    else:
        # Create tenant
        __salt__['keystone.tenant_create'](name, description, enabled)
        ret['comment'] = 'Tenant "{0}" has been added'.format(name)
        ret['changes']['Tenant'] = 'Created'
    return ret


def tenant_absent(name):
    '''
    Ensure that the keystone tenant is absent.

    name
        The name of the tenant that should not exist
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Tenant "{0}" is already absent'.format(name)}

    # Check if tenant is present
    tenant = __salt__['keystone.tenant_get'](name=name)
    if 'Error' not in tenant:
        # Delete tenant
        __salt__['keystone.tenant_delete'](name=name)
        ret['comment'] = 'Tenant "{0}" has been deleted'.format(name)
        ret['changes']['Tenant'] = 'Deleted'

    return ret
