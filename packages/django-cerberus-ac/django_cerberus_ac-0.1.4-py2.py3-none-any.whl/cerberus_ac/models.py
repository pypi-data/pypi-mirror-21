# -*- coding: utf-8 -*-

"""
Models and mixins for access control.

- RoleMixin
- Role
- RoleHierarchy
- RolePrivilege
- PrivilegeHistory
- AccessHistory
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .apps import AppSettings

app_settings = AppSettings()


def get_role_type(role):
    """
    Get a role's type.

    Args:
        role (obj): a Python object.

    Returns:
        str: the role's type.
    """
    if hasattr(role, 'role_type'):
        attr = role.role_type
        if callable(attr):
            return attr()
        return attr
    return app_settings.mapping.name_from_instance(role)


def get_role_id(role):
    """
    Get a role's ID.

    Args:
        role (obj): a Python object.

    Returns:
        str: the role's ID or None.
    """
    if hasattr(role, 'role_id'):
        attr = role.role_id
        if callable(attr):
            return str(attr())
        return str(attr)
    elif hasattr(role, 'id'):
        return str(role.id)
    return ''


def get_role_type_and_id(role, role_id=''):
    """
    Return both type and ID of a role.

    Args:
        role (obj): string or role instance.
        role_id (str): string ID or None.

    Returns:
        tuple: type and ID of role.
    """
    if isinstance(role, str):
        return role, role_id
    return get_role_type(role), get_role_id(role)


def get_resource_type(resource):
    """
    Get a resource's type.

    Args:
        resource (obj): a Python object.

    Returns:
        str: the resource's type.
    """
    if hasattr(resource, 'resource_type'):
        attr = resource.resource_type
        if callable(attr):
            return attr()
        return attr
    return app_settings.mapping.name_from_instance(resource)


def get_resource_id(resource):
    """
    Get a resource's ID.

    Args:
        resource (obj): a Python object.

    Returns:
        str: the resource's ID or None.
    """
    if hasattr(resource, 'resource_id'):
        attr = resource.resource_id
        if callable(attr):
            return attr()
        return attr
    elif hasattr(resource, 'id'):
        return resource.id
    return None


def get_resource_type_and_id(resource, resource_id=''):
    """
    Return both type and ID of a resource.

    Args:
        resource (obj): string or resource instance.
        resource_id (str): string ID or None.

    Returns:
        tuple: type and ID of resource.
    """
    if isinstance(resource, str):
        return resource, resource_id
    return get_resource_type(resource), get_resource_id(resource)


class RoleMixin(object):
    """
    Mixin for Role models / classes.

    This mixin provides shortcuts methods to manipulate and check the
    privileges granted to a role, be it a custom class or Role instance.
    """

    def role_type(self):
        """Return the role type of this instance."""
        return app_settings.mapping.name_from_instance(self)

    def role_id(self):
        """Return the role ID of this instance."""
        if hasattr(self, 'id'):
            return self.id
        return None

    def heirs(self, search=None):
        """Return the children of this role."""
        if search is not None:
            return [app_settings.mapping.instance_from_name_and_id(*h)
                    for h in RoleHierarchy.all_heirs(
                self.role_type(), self.role_id(), search)]
        return [app_settings.mapping.instance_from_name_and_id(*h)
                for h in RoleHierarchy.heirs(self.role_type(), self.role_id())]

    def inherits_from(self, role, role_id=''):
        """
        Check if this role inherits privileges from the given role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (str): only used when role is a string.

        Returns:
            bool: True or False
        """
        role_type, role_id = get_role_type_and_id(role, role_id)
        try:
            RoleHierarchy.objects.get(
                role_type_a=self.role_type(), role_id_a=self.role_id(),
                role_type_b=role_type, role_id_b=role_id)
            return True
        except RoleHierarchy.DoesNotExist:
            return False

    def inherit_from(self, role, role_id=''):
        """
        Set this role as child of the given role.

        The child role will then inherit privileges from the parent role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (str): only used when role is a string.

        Returns:
            obj: the created RoleHierarchy object.
        """
        role_type, role_id = get_role_type_and_id(role, role_id)
        return RoleHierarchy.objects.create(
            role_type_a=self.role_type(), role_id_a=self.role_id(),
            role_type_b=role_type, role_id_b=role_id)

    def conveyors(self, search=None):
        """Return the roles conveying privileges to this role."""
        if search is not None:
            return [app_settings.mapping.instance_from_name_and_id(*c)
                    for c in RoleHierarchy.all_conveyors(
                self.role_type(), self.role_id(), search)]
        return [app_settings.mapping.instance_from_name_and_id(*c)
                for c in RoleHierarchy.conveyors(self.role_type(), self.role_id())]  # noqa

    def conveys_to(self, role, role_id=''):
        """
        Check if this role conveys privileges to the given role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (str): only used when role is a string.

        Returns:
            bool: True or False
        """
        role_type, role_id = get_role_type_and_id(role, role_id)
        try:
            RoleHierarchy.objects.get(
                role_type_a=role_type, role_id_a=role_id,
                role_type_b=self.role_type(), role_id_b=self.role_id())
            return True
        except RoleHierarchy.DoesNotExist:
            return False

    def convey_to(self, role, role_id=''):
        """
        Set this role as parent of the given role.

        The parent role will then transmit privileges to the child role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (str): only used when role is a string.

        Returns:
            obj: the created RoleHierarchy object.
        """
        role_type, role_id = get_role_type_and_id(role, role_id)
        return RoleHierarchy.objects.create(
            role_type_a=role_type, role_id_a=role_id,
            role_type_b=self.role_type(), role_id_b=self.role_id())

    def can(self, perm, resource, resource_id=''):
        """
        Check if this role has privilege ``perm`` on resource.

        Args:
            perm (str): string describing permission or privilege.
            resource (str/obj): a resource instance or a string describing it.
            resource_id (str): only used when resource is a string.

        Returns:
            bool: True or False
        """
        resource_type, resource_id = get_resource_type_and_id(resource, resource_id)  # noqa
        return RolePrivilege.authorize(
            role_type=self.role_type(), role_id=self.role_id(), perm=perm,
            resource_type=resource_type, resource_id=resource_id)


# TODO: write a ResourceMixin class? And the according Resource class?
class ResourceMixin(object):
    """Mixin for Resource models / classes."""


# TODO: is this class useful? Should it just be a class, not a model?
class Role(models.Model, RoleMixin):
    """Concrete model for roles."""

    type = models.CharField(max_length=255)
    rid = models.CharField(max_length=255, blank=True)

    class Meta:
        """Meta class for Django."""

        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        unique_together = ('type', 'rid')

    def __str__(self):
        if self.rid:
            return '%s %s' % (self.type, self.rid)
        return self.type

    def role_type(self):
        """Override role_type method and return type attribute."""
        return self.type

    def role_id(self):
        """Override role_id method and return rid attribute."""
        return self.rid


class RoleHierarchy(models.Model):
    """Role hierarchy model."""

    BREADTH_FIRST = 0
    DEPTH_FIRST = 1

    role_type_a = models.CharField(max_length=255)
    role_id_a = models.CharField(max_length=255, blank=True)
    role_type_b = models.CharField(max_length=255)
    role_id_b = models.CharField(max_length=255, blank=True)

    class Meta:
        """Meta class for Django."""

        verbose_name = _('Role hierarchy')
        verbose_name_plural = _('Role hierarchy')
        unique_together = (
            'role_type_a', 'role_id_a',
            'role_type_b', 'role_id_b'
        )

    def __str__(self):
        a = self.role_type_a
        if self.role_id_a:
            a += ' %s' % self.role_id_a
        b = self.role_type_b
        if self.role_id_b:
            b += ' %s' % self.role_id_b

        return '%s is part of %s' % (a, b)

    @staticmethod
    def conveyors(role_type, role_id):
        """
        Return immediate roles conveying privileges to role_type, role_id.

        Args:
            role_type (str): string describing the role type.
            role_id (str): unique ID of the role.

        Returns:
            list: list of (role_type, role_id) conveyors.
        """
        return [(rh.role_type_b, rh.role_id_b)
                for rh in RoleHierarchy.objects.filter(
                role_type_a=role_type, role_id_a=role_id)]

    @staticmethod
    def heirs(role_type, role_id):
        """
        Return immediate roles inheriting privileges from role_type, role_id.

        Args:
            role_type (str): string describing the role type.
            role_id (str): unique ID of the role.

        Returns:
            list: list of (role_type, role_id) heirs.
        """
        return [(rh.role_type_a, rh.role_id_a)
                for rh in RoleHierarchy.objects.filter(
                role_type_b=role_type, role_id_b=role_id)]

    @staticmethod
    def all_conveyors(role_type, role_id, search=BREADTH_FIRST):
        """
        Return every roles conveying privileges to role_type, role_id.

        Args:
            role_type (str): string describing the role type.
            role_id (str): unique ID of the role.
            search (int): 0: breadth-first, 1: depth-first.

        Returns:
            list: list of (role_type, role_id) conveyors.
        """
        result = []
        if search == RoleHierarchy.DEPTH_FIRST:
            for r in RoleHierarchy.conveyors(role_type, role_id):
                result.append(r)
                result.extend(RoleHierarchy.all_conveyors(r[0], r[1], search))
        else:
            line = RoleHierarchy.conveyors(role_type, role_id)
            result.extend(line)
            for r in line:
                result.extend(RoleHierarchy.all_conveyors(r[0], r[1], search))
        return result

    @staticmethod
    def all_heirs(role_type, role_id, search=BREADTH_FIRST):
        """
        Return every roles inheriting privileges from role_type, role_id.

        Args:
            role_type (str): string describing the role type.
            role_id (str): unique ID of the role.
            search (int): 0: breadth-first, 1: depth-first.

        Returns:
            list: list of (role_type, role_id) heirs.
        """
        result = []
        if search == RoleHierarchy.DEPTH_FIRST:
            for r in RoleHierarchy.heirs(role_type, role_id):
                result.append(r)
                result.extend(RoleHierarchy.all_heirs(r[0], r[1], search))
        else:
            line = RoleHierarchy.heirs(role_type, role_id)
            result.extend(line)
            for r in line:
                result.extend(RoleHierarchy.all_heirs(r[0], r[1], search))
        return result


class RolePrivilege(models.Model):
    """Role privilege model."""

    role_type = models.CharField(_('Role type'), max_length=255)
    role_id = models.CharField(_('Role ID'), max_length=255, blank=True)

    authorized = models.BooleanField(
        _('Authorized'), default=AppSettings.get_default_response())
    access_type = models.CharField(_('Access type'), max_length=255)

    resource_type = models.CharField(_('Resource type'), max_length=255)
    resource_id = models.CharField(_('Resource ID'), max_length=255, blank=True)

    creation_date = models.DateTimeField(_('Created'), auto_now_add=True)
    modification_date = models.DateTimeField(_('Last modified'), auto_now=True)

    class Meta:
        """Meta class for Django."""

        verbose_name = _('Role privilege')
        verbose_name_plural = _('Role privileges')
        unique_together = (
            'role_type', 'role_id',
            'access_type',
            'resource_type', 'resource_id'
        )

    def __str__(self):
        return '%s %s %s to %s %s %s' % (
            'allow' if self.authorized else 'deny', self.role_type,
            self.role_id if self.role_id else '', self.access_type,
            self.resource_type, self.resource_id if self.resource_id else '')

    @staticmethod
    def authorize(role_type,
                  role_id,
                  perm,
                  resource_type,
                  resource_id,
                  skip_implicit=None,
                  log=None):
        """
        Authorize access to a resource to a role.

        This method checks if a role has access to a resource or a type of
        resource. Calling this method will also try to record an entry log
        in the corresponding access attempt model.

        Call will not break if there is no access attempt model. Simply,
        nothing will be recorded.

        Args:
            role_type (str): the string describing the role.
            role_id (str): the unique ID of the role.
            perm (Permission's constant): one of the permissions available
                in Permission class.
            resource_type (str): the string describing the resource.
            resource_id (str): the unique ID of the resource.
            log (bool): record an entry in access history model or not.
            skip_implicit (bool): whether to skip implicit authorization.
                It will always be skipped if you set ACCESS_CONTROL_IMPLICIT
                setting to False.

        Returns:
            bool: role has perm on resource (or not).
        """
        if skip_implicit is None:
            skip_implicit = AppSettings.get_skip_implicit()

        if log is None:
            log = AppSettings.get_log_access()

        attempt = AccessHistory(role_type=role_type, role_id=role_id,
                                resource_type=resource_type,
                                resource_id=resource_id, access_type=perm)
        attempt.response = None
        attempt.response_type = AccessHistory.EXPLICIT

        # Check role explicit perms
        attempt.response = RolePrivilege.authorize_explicit(
            role_type, role_id, perm, resource_type, resource_id)

        if attempt.response is None:

            # Else check inherited explicit perms
            for above_role_type, above_role_id in RoleHierarchy.all_conveyors(role_type, role_id):  # noqa
                attempt.response = RolePrivilege.authorize_explicit(
                    above_role_type, above_role_id, perm,
                    resource_type, resource_id)

                if attempt.response is not None:
                    attempt.inherited_type = above_role_type
                    attempt.inherited_id = above_role_id
                    break

        # Else check role implicit perms
        # TODO: uncomment this when implicit mechanisms are implemented
        # if attempt.response is None and not skip_implicit:
        #     attempt.response = RolePrivilege.authorize_implicit(
        #         role_type, role_id, perm, resource_type, resource_id)
        #
        #     if attempt.response is not None:
        #         attempt.response_type = AccessHistory.IMPLICIT
        #
        #     # Else check inherited implicit perms
        #     else:
        #
        #         for above_role_type, above_role_id in RoleHierarchy.all_conveyors(role_type, role_id):  # noqa
        #             attempt.response = RolePrivilege.authorize_implicit(
        #                 above_role_type, above_role_id, perm,
        #                 resource_type, resource_id)
        #
        #             if attempt.response is not None:
        #                 attempt.response_type = AccessHistory.IMPLICIT
        #                 attempt.inherited_type = above_role_type
        #                 attempt.inherited_id = above_role_id
        #                 break

        # Else give default response
        if attempt.response is None:
            attempt.response = AppSettings.get_default_response()
            attempt.response_type = AccessHistory.DEFAULT

        if log:
            attempt.save()

        return attempt.response

    @staticmethod
    def authorize_explicit(role_type,
                           role_id,
                           perm,
                           resource_type,
                           resource_id=''):
        """
        Run an explicit authorization check.

        Args:
            role_type (str): a string describing the type of role.
            role_id (str): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (str): the resource's ID.

        Returns:

        """
        try:
            privilege = RolePrivilege.objects.get(
                role_type=role_type, role_id=role_id,
                resource_type=resource_type, resource_id=resource_id,
                access_type=perm)
            return privilege.authorized
        except RolePrivilege.DoesNotExist:
            return None

    # TODO: implement this in some way
    @staticmethod
    def authorize_implicit(role_type,
                           role_id,
                           perm,
                           resource_type,
                           resource_id=''):
        """
        Run an implicit authorization check.

        This method checks that the given permission can be implicitly
        obtained through the ``implicit_perms`` method.

        Args:
            role_type (str): a string describing the type of role.
            role_id (str): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (str): the resource's ID.

        Returns:
            bool: denied(perm) or allowed(perm) found in implicit_perms().
            None: if ACCESS_CONTROL_IMPLICIT is False,
                or perm is in ignored_perms.
        """
        return None

    @staticmethod
    def allow(role_type,
              role_id,
              perm,
              resource_type,
              resource_id='',
              user=None,
              log=True):
        """
        Explicitly give perm to role on resource.

        Args:
            role_type (str): a string describing the type of role.
            role_id (str): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (str): the resource's ID.
            user (User): an instance of settings.AUTH_USER_MODEL.
            log (bool): whether to record an entry in privileges history.

        Returns:
            access instance: the created privilege.
        """
        privilege, created = RolePrivilege.objects.update_or_create(
            role_type=role_type,
            role_id=role_id,
            access_type=perm,
            resource_type=resource_type,
            resource_id=resource_id,
            defaults={'authorized': True})

        if log:
            record = PrivilegeHistory(
                user=user, action={True: PrivilegeHistory.CREATE}.get(
                    created, PrivilegeHistory.UPDATE))
            record.update_from_privilege(privilege)

        return privilege, created

    @staticmethod
    def deny(role_type,
             role_id,
             perm,
             resource_type,
             resource_id='',
             user=None,
             log=True):
        """
        Explicitly remove perm to role on resource.

        Args:
            role_type (str): a string describing the type of role.
            role_id (str): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (str): the resource's ID.
            user (User): an instance of settings.AUTH_USER_MODEL.
            log (bool): whether to record an entry in privileges history.

        Returns:
            access instance: the created privilege.
        """
        privilege, created = RolePrivilege.objects.update_or_create(
            role_type=role_type,
            role_id=role_id,
            access_type=perm,
            resource_type=resource_type,
            resource_id=resource_id,
            defaults={'authorized': False})

        if log:
            record = PrivilegeHistory(
                user=user, action={True: PrivilegeHistory.CREATE}.get(
                    created, PrivilegeHistory.UPDATE))
            record.update_from_privilege(privilege)

        return privilege, created

    @staticmethod
    def forget(role_type,
               role_id,
               perm,
               resource_type,
               resource_id='',
               user=None,
               log=True):
        """
        Forget any privilege present between role and resource.

        Args:
            role_type (str): a string describing the type of role.
            role_id (str): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (str): the resource's ID.
            user (User): an instance of settings.AUTH_USER_MODEL.
            log (bool): whether to record an entry in privileges history.

        Returns:
            int, dict:
                the number of privileges deleted and a dictionary with the
                number of deletions per object type (django's delete return).
        """
        try:
            privilege = RolePrivilege.objects.get(
                role_type=role_type, role_id=role_id,
                resource_type=resource_type, resource_id=resource_id,
                access_type=perm)

            if log:
                record = PrivilegeHistory(
                    user=user, action=PrivilegeHistory.DELETE)
                record.update_from_privilege(privilege)

            privilege.delete()
            return True
        except RolePrivilege.DoesNotExist:
            return False


# TODO: implement HierarchyHistory model?


class PrivilegeHistory(models.Model):
    """Privilege history model."""

    CREATE = 'c'
    # READ = 'r'  # makes no sense here
    UPDATE = 'u'
    DELETE = 'd'

    ACTIONS_VERBOSE = {
        CREATE: 'create',
        # READ: 'read',
        UPDATE: 'update',
        DELETE: 'delete'
    }

    ACTIONS = (
        (CREATE, _(ACTIONS_VERBOSE[CREATE])),
        # (READ, _(ACTIONS_VERBOSE[READ])),
        (UPDATE, _(ACTIONS_VERBOSE[UPDATE])),
        (DELETE, _(ACTIONS_VERBOSE[DELETE])),
    )

    privilege_id = models.PositiveIntegerField(
        _('Privilege reference ID'), null=True)
    reference = models.ForeignKey(
        RolePrivilege, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Privilege reference'), related_name='history')
    action = models.CharField(_('Action'), max_length=1, choices=ACTIONS)
    datetime = models.DateTimeField(_('Date and time'), auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        verbose_name=_('User'), related_name='privileges_changes',
        null=True)

    role_type = models.CharField(_('Role type'), max_length=255, blank=True)
    role_id = models.CharField(_('Role ID'), max_length=255, blank=True)

    authorized = models.NullBooleanField(_('Authorization'), default=None)
    access_type = models.CharField(
        _('Access type'), max_length=255, blank=True)

    resource_type = models.CharField(
        _('Resource type'), max_length=255, blank=True)
    resource_id = models.CharField(_('Resource ID'), max_length=255, blank=True)  # noqa

    class Meta:
        """Meta class for Django."""

        verbose_name = _('Privilege history')
        verbose_name_plural = _('Privilege history')

    def __str__(self):
        if self.reference:
            privilege = str(self.reference)
        else:
            privilege = RolePrivilege(
                role_type=self.role_type,
                role_id=self.role_id,
                authorized=self.authorized,
                access_type=self.access_type,
                resource_type=self.resource_type,
                resource_id=self.resource_id)

        return '[%s] user %s has %sd privilege <%d: %s>' % (
            self.datetime, self.user,
            PrivilegeHistory.ACTIONS_VERBOSE[str(self.action)],
            self.privilege_id, privilege)

    def update_from_privilege(self, privilege, save=True):
        """
        Update this object with given privilege's attributes.

        Args:
            privilege (RolePrivilege): privilege to update from.
            save (bool): whether to commit the changes to the database.
        """
        self.reference = privilege
        self.privilege_id = privilege.id
        self.role_type = privilege.role_type
        self.role_id = privilege.role_id
        self.authorized = privilege.authorized
        self.access_type = privilege.access_type
        self.resource_type = privilege.resource_type
        self.resource_id = privilege.resource_id
        if save:
            self.save()


class AccessHistory(models.Model):
    """Access history model."""

    DEFAULT = 'd'
    IMPLICIT = 'i'
    EXPLICIT = 'e'

    RESPONSE_TYPE_VERBOSE = {
        DEFAULT: 'by default',
        IMPLICIT: 'implicitly',
        EXPLICIT: 'explicitly'
    }

    RESPONSE_TYPE = (
        (DEFAULT, _(RESPONSE_TYPE_VERBOSE[DEFAULT])),
        (IMPLICIT, _(RESPONSE_TYPE_VERBOSE[IMPLICIT])),
        (EXPLICIT, _(RESPONSE_TYPE_VERBOSE[EXPLICIT]))
    )

    role_type = models.CharField(_('Role type'), max_length=255, blank=True)
    role_id = models.CharField(_('Role ID'), max_length=255, blank=True)

    # We don't want to store false info, None says "we don't know"
    response = models.NullBooleanField(_('Response'), default=None)
    response_type = models.CharField(
        _('Response type'), max_length=1, choices=RESPONSE_TYPE)
    access_type = models.CharField(_('Access'), max_length=255)

    resource_type = models.CharField(_('Resource type'), max_length=255)
    resource_id = models.CharField(_('Resource ID'), max_length=255, blank=True)  # noqa

    datetime = models.DateTimeField(_('Date and time'), default=timezone.now)

    conveyor_type = models.CharField(_('Conveyor type'), max_length=255, blank=True)  # noqa
    conveyor_id = models.CharField(_('Conveyor ID'), max_length=255, blank=True)  # noqa

    class Meta:
        """Meta class for Django."""

        verbose_name = _('Access history')
        verbose_name_plural = _('Access history')

    def __str__(self):
        inherited = ''

        if self.role_id:
            role = '%s %s' % (self.role_type, self.role_id)
        else:
            role = self.role_type

        if self.conveyor_type:
            if self.conveyor_id:
                inherited = ' (inherited from %s %s)' % (
                    self.conveyor_type, self.conveyor_id)
            else:
                inherited = self.conveyor_type

        authorized = 'authorized' if self.response else 'unauthorized'
        string = '[%s] %s was %s %s to %s %s %s' % (
            self.datetime, role,
            AccessHistory.RESPONSE_TYPE_VERBOSE[str(self.response_type)],
            authorized, self.access_type, self.resource_type, self.resource_id)
        if inherited:
            return string + inherited
        return string
