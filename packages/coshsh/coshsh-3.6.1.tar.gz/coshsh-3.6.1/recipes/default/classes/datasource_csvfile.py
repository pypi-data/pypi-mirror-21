#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#
# Copyright 2010-2012 Gerhard Lausser.
# This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

import csv
import os
import re
import logging
from copy import copy
import coshsh
from coshsh.datasource import Datasource, DatasourceNotAvailable
from coshsh.host import Host
from coshsh.application import Application
from coshsh.contactgroup import ContactGroup
from coshsh.contact import Contact
from coshsh.monitoringdetail import MonitoringDetail
from coshsh.util import compare_attr

logger = logging.getLogger('coshsh')

def __ds_ident__(params={}):
    if coshsh.util.compare_attr("type", params, "csv"):
        return CsvFile

class CommentedFile:
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring
    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line
    def __iter__(self):
        return self

class CsvFile(coshsh.datasource.Datasource):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.name = kwargs["name"]
        self.dir = kwargs["dir"]
        self.objects = {}

    def open(self):
        logger.info('open datasource %s' % self.name)
        if not os.path.exists(self.dir):
            logger.error('csv dir %s does not exist' % self.dir)
            raise coshsh.datasource.DatasourceNotAvailable

    def read(self, filter=None, objects={}, force=False, **kwargs):
        self.objects = objects
        try:
            hostreader = csv.DictReader(CommentedFile(open(os.path.join(self.dir, self.name+'_hosts.csv'))))
            logger.info('read hosts from %s' % os.path.join(self.dir, self.name+'_hosts.csv'))
        except Exception, exp:
            print "except", exp
            hostreader = []
        # host_name,address,type,os,hardware,virtual,notification_period,location,department
        for row in hostreader:
            row["templates"] = ["generic-host"]
            for attr in [k for k in row.keys() if k in ['type', 'os', 'hardware', 'virtual']]:
                try:
                    row[attr] = row[attr].lower()
                except Exception:
                    pass
            h = coshsh.host.Host(row)
            self.add('hosts', h)

        try:
            appreader = csv.DictReader(CommentedFile(open(os.path.join(self.dir, self.name+'_applications.csv'))))
            logger.info('read applications from %s' % os.path.join(self.dir, self.name+'_applications.csv'))
        except Exception, e:
            appreader = []
        resolvedrows = []
        # name,type,component,version,host_name,check_period
        for row in appreader:
            for attr in [k for k in row.keys() if k in ['name', 'type', 'component', 'version']]:
                try:
                    row[attr] = row[attr].lower()
                except Exception:
                    pass
            if '[' in row['host_name'] or '*' in row['host_name']:
                # hostnames can be regular expressions
                matching_hosts = [h for h in self.objects['hosts'].keys() if re.match('^('+row['host_name']+')', h)]
                for host_name in matching_hosts:
                    row['host_name'] = host_name
                    resolvedrows.append(copy(row))
            else:
                resolvedrows.append(copy(row))
        for row in resolvedrows:
            a = coshsh.application.Application(row)
            self.add('applications', a)

        try:
            appdetailreader = csv.DictReader(CommentedFile(open(os.path.join(self.dir, self.name+'_applicationdetails.csv'))))
            logger.info('read appdetails from %s' % os.path.join(self.dir, self.name+'_applicationdetails.csv'))
        except Exception:
            appdetailreader = []
        resolvedrows = []
        # host_name,name,type,monitoring_type,monitoring_0,monitoring_1,monitoring_2,monitoring_3,monitoring_4,monitoring_5
        for row in appdetailreader:
            if '[' in row['host_name'] or '*' in row['host_name']:
                # hostnames can be regular expressions
                matching_hosts = [h for h in self.objects['hosts'].keys() if re.match('^('+row['host_name']+')', h)]
                for host_name in matching_hosts:
                    row['host_name'] = host_name
                    resolvedrows.append(copy(row))
            else:
                resolvedrows.append(copy(row))
        for row in resolvedrows:
            for attr in [k for k in row.keys() if k in ['name', 'type', 'component', 'version']]:
                row[attr] = row[attr].lower()
            application_id = "%s+%s+%s" % (row["host_name"], row["name"], row["type"])
            detail = coshsh.monitoringdetail.MonitoringDetail(row)
            self.add('details', detail)
        
        try:
            contactgroupreader = csv.DictReader(CommentedFile(open(os.path.join(self.dir, self.name+'_contactgroups.csv'))))
            logger.info('read contactgroups from %s' % os.path.join(self.dir, self.name+'_contactgroups.csv'))
        except Exception:
            contactgroupreader = []
        resolvedrows = []
        # host_name,name,type,groups
        for row in contactgroupreader:
            if '[' in row['host_name'] or '*' in row['host_name']:
                # hostnames can be regular expressions
                matching_hosts = [h for h in self.objects['hosts'].keys() if re.match('^('+row['host_name']+')', h)]
                for host_name in matching_hosts:
                    row['host_name'] = host_name
                    resolvedrows.append(copy(row))
            else:
                resolvedrows.append(copy(row))
        for row in resolvedrows:
            application_id = "%s+%s+%s" % (row["host_name"], row["name"], row["type"])
            for group in row["groups"].split(":"):
                if not self.find('contactgroups', group):
                    self.add('contactgroups', coshsh.contactgroup.ContactGroup({ 'contactgroup_name' : group }))
                if self.find('applications', application_id) and row["name"] == "os":
                    if not group in self.get('applications', application_id).contact_groups:
                        self.get('applications', application_id).contact_groups.append(group)
                    # OS contacts also are host's contacts
                    if not group in self.get('hosts', row["host_name"]).contact_groups:
                        self.get('hosts', row["host_name"]).contact_groups.append(group)
                elif self.find('applications', application_id):
                    if not group in self.get('applications', application_id).contact_groups:
                        self.get('applications', application_id).contact_groups.append(group)
                elif ("name" not in row or not row['name']) and self.find('hosts', row['host_name']):
                    if not group in self.get('hosts', row['host_name']).contact_groups:
                        self.get('hosts', row['host_name']).contact_groups.append(group)
                else:
                    logger.error('no such application %s for contactgroup %s' % (application_id, row['groups']))

        
        try:
            contactreader = csv.DictReader(CommentedFile(open(os.path.join(self.dir, self.name+'_contacts.csv'))))
            logger.info('read contacts from %s' % os.path.join(self.dir, self.name+'_contacts.csv'))
        except Exception:
            contactreader = []
        # name,type,address,userid,notification_period,groups
        for row in contactreader:
            c = coshsh.contact.Contact(row)
            if not self.find('contacts', c.fingerprint()):
                c.contactgroups.extend(row["groups"].split(":"))
                self.add('contacts', c)


