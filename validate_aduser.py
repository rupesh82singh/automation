#!/usr/bin/env python

import ldap
import ldap.modlist
import dns.resolver
import getpass


def get_ldap_hosts(domain):
    ldap_srv = dns.resolver.resolve('_ldap._tcp.%s.' % domain, 'SRV')
    return [str(srv.target) for srv in ldap_srv]


def get_search_base(domain):
    return ",".join("dc=%s" % i for i in domain.split('.'))


def isuser(email, ldap):
    email = fix_mail(email)
    user_obj = ldap.search_mail_or_proxyAddresses(email)
    key = ['mail','proxyAddresses']
    value = [email, 'smtp:'+email]
    if user_obj[0] != None and key != None and value != None:
        if not isinstance(key, list):
            key = [key]
        if not isinstance(value, list):
            value = [value]
        for k, v in zip(key, value):
            v = bytes(v, "utf-8")
            if k in user_obj[0][1] and v in user_obj[0][1][k]:
                return True
        return False
    if len(user_obj) >= 4:
        return True
    return False


class LdapSearch(object):
    def __init__(self, userprincipal, Secret):
        self.DN = userprincipal

        principal = userprincipal.split('@')
        domain = principal[1]

        self.ldap_hosts = get_ldap_hosts(domain)
        self.ldap_schema = "ldaps://%s"

        self.Server = self.ldap_schema % self.ldap_hosts[0]

        self.Base = get_search_base(domain)
        self.Scope = ldap.SCOPE_SUBTREE
        self.Attrs = ["*"]

        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

        self.l = ldap.initialize(self.Server)
        self.l.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        self.l.set_option(ldap.OPT_X_TLS_DEMAND, True)
        self.l.protocol_version = 3
        self.l.set_option(ldap.OPT_REFERRALS, 0)

        self.l.simple_bind_s(self.DN, Secret)

    def filter_samaccountname_enabled(self, sAMAccountName):
        return f"(&(objectClass=user)(sAMAccountName={sAMAccountName})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))"

    def filter_mail_enabled(self, mail):
        return f"(&(objectClass=user)(mail={mail})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))"

    def filter_proxyAddresses_enabled(self, proxyAddresses):
        return f"(&(objectClass=user)(proxyAddresses={proxyAddresses})(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))"

    def filter_mail_or_proxyAddresses_enabled(self, mail):
        return f"(&(objectClass=user)(|(proxyAddresses=smtp:{mail})(mail={mail}))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))"

    def filter_group(self):
        return f"(objectClass=group)"

    def filter_users_of_group(self, groupCN):
        return f"(memberOf:1.2.840.113556.1.4.1941:={groupCN})"

    def search(self, username):
        return self.l.search_s(self.Base, self.Scope, self.filter_samaccountname_enabled(username), self.Attrs)

    def search_mail(self, mail):
        return self.l.search_s(self.Base, self.Scope, self.filter_mail_enabled(mail), self.Attrs)

    def search_proxyAddresses(self, proxyAddresses):
        return self.l.search_s(self.Base, self.Scope, self.filter_proxyAddresses_enabled(proxyAddresses), self.Attrs)

    def search_mail_or_proxyAddresses(self, mail):
        return self.l.search_s(self.Base, self.Scope, self.filter_mail_or_proxyAddresses_enabled(mail), self.Attrs)

    def search_groups(self, base):
        return self.l.search_s(base, self.Scope, self.filter_group(), self.Attrs)


def getconnection():
    import os
    ad_username = os.getenv("AD_USER_PRINCIPAL")
    password = os.getenv("AD_USER_PASSWORD")
    if not ad_username:
        ad_username = input("enter your user principal (username@domain): ")
    if not password:
        password = getpass.getpass(f"enter your password for {ad_username}: ")
    print()
    return LdapSearch(ad_username, password)


def fix_proxyAddress(attr):
    if not "@" in attr:
        attr = f"smtp:{attr}@malwarebytes.com"
    else:
        if not "smtp:" in attr:
            attr = f"smtp:{attr}"
    return attr


def fix_mail(attr):
    if not "@" in attr:
        attr = f"{attr}@malwarebytes.com"
    return attr
