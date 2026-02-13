# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2024  Nexedi SA and Contributors.
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.
#
##############################################################################

from erp5.component.test.testSlapOSERP5VirtualMasterScenario import TestSlapOSVirtualMasterScenarioMixin
from erp5.component.test.SlapOSTestCaseMixin import PinnedDateTime
from DateTime import DateTime

class TestSlapOSERP5WorkgroupScenario(TestSlapOSVirtualMasterScenarioMixin):

  def test_virtual_master_without_accounting_workgroup_scenario(self):
    with PinnedDateTime(self, DateTime('2024/02/17')):
      currency, _, _, sale_person, _ = self.bootstrapVirtualMasterTest(is_virtual_master_accountable=False)

      # lets join as slapos administrator, which will own few compute_nodes
      owner_reference = 'owner-%s' % self.generateNewId()
      owner_person = self.joinSlapOS(owner_reference)

      self.login(sale_person.getUserId())

      # create a default project
      project = self.addDefaultProject(
        person=owner_person, currency=currency)

      self.login(owner_person.getUserId())
      public_server_title = 'Public Server for %s' % owner_reference
      public_server = self.requestComputeNode(public_server_title, project.getReference())

      # and install some software on them
      public_server_software = self.generateNewSoftwareReleaseUrl()
      public_instance_type = 'public type'

      self.supplySoftware(public_server, public_server_software)

      # format the compute_nodes
      self.formatComputeNode(public_server)

      software_product, release_variation, type_variation = self.addSoftwareProduct(
        "instance product", project, public_server_software, public_instance_type
      )

      self.addAllocationSupply("for compute node", public_server, software_product,
                               release_variation, type_variation)

      self.tic()
      self.login()
      self.checkServiceSubscriptionRequest(public_server)

      # join as the another visitor and request software instance on public
      # compute_node
      public_reference = 'public-%s' % self.generateNewId()
      public_person = self.joinSlapOS(public_reference)

      self.login(public_person.getUserId())
      workgroup = self.createWorkgroup(
        public_person, project)
      self.tic()

    with PinnedDateTime(self, DateTime('2024/02/17 01:01')):
      public_instance_title = 'Public title %s' % self.generateNewId()
      self.checkInstanceAllocation(public_person.getUserId(),
          public_reference, public_instance_title,
          public_server_software, public_instance_type,
          public_server, project.getReference(), workgroup)

      self.login(owner_person.getUserId())

      # and the instances
      self.checkInstanceUnallocation(public_person.getUserId(),
          public_reference, public_instance_title,
          public_server_software, public_instance_type, public_server,
          project.getReference(), workgroup)

      # and uninstall some software on them
      self.removeSoftwareReleaseFromComputeNode(owner_person,
        public_server, public_server_software)

    # Ensure no unexpected object has been created
    # 3 allocation supply, line, cell
    # 3 assignment request
    # 1 compute node
    # 1 credential request
    # 1 instance tree
    # 3 open sale order XXX * 2 why
    # 3 assignment
    # 3 simulation movement
    # 3 sale packing list / line
    # 2 sale trade condition ( a 3rd trade condition is not linked to the project)
    # 1 software installation
    # 1 software instance
    # 1 software product
    # 3 subscription request
    self.assertRelatedObjectCount(project, 34)

    with PinnedDateTime(self, DateTime('2024/02/18 01:01')):
      self.checkERP5StateBeforeExit()