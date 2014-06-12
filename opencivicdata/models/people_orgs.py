from django.db import models
from .base import OCDBase, LinkBase, OCDIDField, RelatedBase
from .jurisdiction import Jurisdiction
from .. import common

# abstract models

class ContactDetailBase(RelatedBase):
    type = models.CharField(max_length=50, choices=common.CONTACT_TYPE_CHOICES)
    value = models.CharField(max_length=300)
    note = models.CharField(max_length=300, blank=True)
    label = models.CharField(max_length=300, blank=True)

    class Meta:
        abstract = True


class IdentifierBase(RelatedBase):
    identifier = models.CharField(max_length=300)
    scheme = models.CharField(max_length=300)

    class Meta:
        abstract = True


class OtherNameBase(RelatedBase):
    name = models.CharField(max_length=500)
    note = models.CharField(max_length=500, blank=True)
    start_date = models.CharField(max_length=10)    # YYYY[-MM[-DD]]
    end_date = models.CharField(max_length=10)      # YYYY[-MM[-DD]]

    class Meta:
        abstract = True


# the actual models

class Organization(OCDBase):
    id = OCDIDField(ocd_type='organization')
    name = models.CharField(max_length=300)
    image = models.URLField(blank=True)
    parent = models.ForeignKey('self', related_name='children', null=True)
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='organizations', null=True)
    classification = models.CharField(max_length=100, blank=True,
                                      choices=common.ORGANIZATION_CLASSIFICATION_CHOICES)
    chamber = models.CharField(max_length=10, blank=True)
    founding_date = models.CharField(max_length=10, blank=True)     # YYYY[-MM[-DD]]
    dissolution_date = models.CharField(max_length=10, blank=True)  # YYYY[-MM[-DD]]


class OrganizationIdentifier(IdentifierBase):
    organization = models.ForeignKey(Organization, related_name='identifiers')


class OrganizationName(OtherNameBase):
    organization = models.ForeignKey(Organization, related_name='other_names')


class OrganizationContactDetail(ContactDetailBase):
    organization = models.ForeignKey(Organization, related_name='contact_details')


class OrganizationLink(LinkBase):
    organization = models.ForeignKey(Organization, related_name='links')


class OrganizationSource(LinkBase):
    organization = models.ForeignKey(Organization, related_name='sources')


class Post(OCDBase):
    id = OCDIDField(ocd_type='post')
    label = models.CharField(max_length=300)
    role = models.CharField(max_length=300, blank=True)
    organization = models.ForeignKey(Organization, related_name='posts')
    start_date = models.CharField(max_length=10)    # YYYY[-MM[-DD]]
    end_date = models.CharField(max_length=10)    # YYYY[-MM[-DD]]


class PostContactDetail(ContactDetailBase):
    post = models.ForeignKey(Post, related_name='contact_details')


class PostLink(LinkBase):
    post = models.ForeignKey(Post, related_name='links')


class Person(OCDBase):
    id = OCDIDField(ocd_type='person')
    name = models.CharField(max_length=300)
    # family_name, given_name, additional_name, honorific_prefix, honorifix_suffix, patronymic_name
    # email
    sort_name = models.CharField(max_length=100, default='')

    image = models.URLField(blank=True)
    gender = models.CharField(max_length=100)
    summary = models.CharField(max_length=500)
    national_identity = models.CharField(max_length=300)
    biography = models.TextField()
    birth_date = models.CharField(max_length=10, blank=True)    # YYYY[-MM[-DD]]
    death_date = models.CharField(max_length=10, blank=True)    # YYYY[-MM[-DD]]


class PersonIdentifier(IdentifierBase):
    person = models.ForeignKey(Person, related_name='identifiers')


class PersonName(OtherNameBase):
    person = models.ForeignKey(Person, related_name='other_names')


class PersonContactDetail(ContactDetailBase):
    person = models.ForeignKey(Person, related_name='contact_details')


class PersonLink(LinkBase):
    person = models.ForeignKey(Person, related_name='links')


class PersonSource(LinkBase):
    person = models.ForeignKey(Person, related_name='sources')


class Membership(OCDBase):
    id = OCDIDField(ocd_type='membership')
    organization = models.ForeignKey(Organization, related_name='memberships')
    person = models.ForeignKey(Person, related_name='memberships')
    post = models.ForeignKey(Post, related_name='memberships', null=True)
    on_behalf_of = models.ForeignKey(Organization, related_name='memberships_on_behalf_of',
                                     null=True)
    label = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=300, blank=True)
    start_date = models.CharField(max_length=10, blank=True)    # YYYY[-MM[-DD]]
    end_date = models.CharField(max_length=10, blank=True)      # YYYY[-MM[-DD]]


class MembershipContactDetail(ContactDetailBase):
    membership = models.ForeignKey(Membership, related_name='contact_details')


class MembershipLink(LinkBase):
    membership = models.ForeignKey(Membership, related_name='links')
