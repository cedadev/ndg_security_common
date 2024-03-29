#!/usr/bin/env python
"""NDG Attribute Authority SAML SOAP Binding client unit tests

NERC DataGrid Project
"""
__author__ = "P J Kershaw"
__date__ = "15/02/10 (moved from test_attributeauthorityclient)"
__copyright__ = "(C) 2010 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
import logging
logging.basicConfig(level=logging.DEBUG)
import os
from os import path, environ
from datetime import datetime
import unittest
from uuid import uuid4
from urllib.error import URLError

from ndg.security.common.config import importElementTree
ElementTree = importElementTree()

from ndg.saml.common import SAMLVersion
from ndg.saml.common.xml import SAMLConstants
from ndg.saml.xml.etree import AttributeQueryElementTree, ResponseElementTree
from ndg.saml.saml2.core import (Subject, Issuer, Attribute, NameID, 
                                 AttributeQuery, XSStringAttributeValue)

from ndg.saml.utils.factory import AttributeQueryFactory

from ndg.saml.saml2.binding.soap.client import SOAPBinding
from ndg.saml.saml2.binding.soap.client.attributequery import (
                                        AttributeQuerySOAPBinding, 
                                        AttributeQuerySslSOAPBinding)
from ndg.security.common.saml_utils.esgf import (ESGFSamlNamespaces,
                                                 ESGFDefaultQueryAttributes,
                                                 ESGFGroupRoleAttributeValue)
from ndg.security.common.test.unit.base import BaseTestCase
from ndg.security.common.utils.configfileparsers import (
    CaseSensitiveConfigParser)


class AttributeAuthoritySAMLInterfaceTestCase(BaseTestCase):
    """NDG Attribute Authority SAML SOAP Binding client unit tests"""

    HERE_DIR = os.path.dirname(__file__)
    CONFIG_FILENAME = 'test_samlattributeauthorityclient.cfg'
    CONFIG_FILEPATH = os.path.join(HERE_DIR, CONFIG_FILENAME)
    
    def __init__(self, *arg, **kw):
        super(AttributeAuthoritySAMLInterfaceTestCase, self).__init__(*arg, 
                                                                      **kw)

        if 'NDGSEC_AACLNT_UNITTEST_DIR' not in environ:
            environ['NDGSEC_AACLNT_UNITTEST_DIR'
                                        ] = path.abspath(path.dirname(__file__))

        self.cfgParser = CaseSensitiveConfigParser()
        self.cfg_filepath = path.join(environ['NDGSEC_AACLNT_UNITTEST_DIR'],
                                     self.__class__.CONFIG_FILENAME)
        self.cfgParser.read(self.cfg_filepath)
        
        self.cfg = {}
        for section in self.cfgParser.sections():
            self.cfg[section] = dict(self.cfgParser.items(section))
    
    def test01AttributeQuery(self):
        _cfg = self.cfg['test01AttributeQuery']
        
        attribute_query = AttributeQuery()
        attribute_query.version = SAMLVersion(SAMLVersion.VERSION_20)
        attribute_query.id = str(uuid4())
        attribute_query.issueInstant = datetime.utcnow()
        
        attribute_query.issuer = Issuer()
        attribute_query.issuer.format = Issuer.X509_SUBJECT
        attribute_query.issuer.value = "/CN=Authorisation Service/O=Site A"    
                        
        attribute_query.subject = Subject()
        attribute_query.subject.nameID = NameID()
        attribute_query.subject.nameID.format = \
            ESGFSamlNamespaces.NAMEID_FORMAT #@UndefinedVariable
        attribute_query.subject.nameID.value = _cfg['subject']
        xsStringNs = SAMLConstants.XSD_NS+"#"+\
                                        XSStringAttributeValue.TYPE_LOCAL_NAME
        fnAttribute = Attribute()
        fnAttribute.name = ESGFSamlNamespaces.FIRSTNAME_ATTRNAME #@UndefinedVariable
        fnAttribute.nameFormat = xsStringNs
        fnAttribute.friendlyName = "FirstName"

        attribute_query.attributes.append(fnAttribute)
    
        lnAttribute = Attribute()
        lnAttribute.name = ESGFSamlNamespaces.LASTNAME_ATTRNAME #@UndefinedVariable
        lnAttribute.nameFormat = xsStringNs
        lnAttribute.friendlyName = "LastName"

        attribute_query.attributes.append(lnAttribute)
    
        emailAddressAttribute = Attribute()
        emailAddressAttribute.name = ESGFSamlNamespaces.EMAILADDRESS_ATTRNAME #@UndefinedVariable
        emailAddressAttribute.nameFormat = xsStringNs
        emailAddressAttribute.friendlyName = "emailAddress"
        
        attribute_query.attributes.append(emailAddressAttribute) 

        siteAAttribute = Attribute()
        siteAAttribute.name = _cfg['siteAttributeName']
        siteAAttribute.nameFormat = xsStringNs
        
        attribute_query.attributes.append(siteAAttribute) 

        binding = SOAPBinding()
        binding.serialise = AttributeQueryElementTree.toXML
        binding.deserialise = ResponseElementTree.fromXML
        
        self.assertRaises(URLError, binding.send, attribute_query, _cfg['uri'])
             
    def test02AttributeQueryInvalidIssuer(self):
        _cfg = self.cfg['test02AttributeQueryInvalidIssuer']
        
        attribute_query = AttributeQuery()
        attribute_query.version = SAMLVersion(SAMLVersion.VERSION_20)
        attribute_query.id = str(uuid4())
        attribute_query.issueInstant = datetime.utcnow()
        
        attribute_query.issuer = Issuer()
        attribute_query.issuer.format = Issuer.X509_SUBJECT
        attribute_query.issuer.value = "/O=Invalid Site/CN=PDP"    
                        
        attribute_query.subject = Subject()  
        attribute_query.subject.nameID = NameID()
        attribute_query.subject.nameID.format = \
            ESGFSamlNamespaces.NAMEID_FORMAT #@UndefinedVariable
        attribute_query.subject.nameID.value = _cfg['subject']
        xsStringNs = SAMLConstants.XSD_NS+"#"+\
                                        XSStringAttributeValue.TYPE_LOCAL_NAME

        siteAAttribute = Attribute()
        siteAAttribute.name = _cfg['siteAttributeName']
        siteAAttribute.nameFormat = xsStringNs
        
        attribute_query.attributes.append(siteAAttribute) 

        binding = SOAPBinding()
        binding.serialise = AttributeQueryElementTree.toXML
        binding.deserialise = ResponseElementTree.fromXML
        
        self.assertRaises(URLError, binding.send, attribute_query, _cfg['uri'])
                   
    def test03AttributeQueryUnknownSubject(self):
        _cfg = self.cfg['test03AttributeQueryUnknownSubject']
        
        attribute_query = AttributeQuery()
        attribute_query.version = SAMLVersion(SAMLVersion.VERSION_20)
        attribute_query.id = str(uuid4())
        attribute_query.issueInstant = datetime.utcnow()
        
        attribute_query.issuer = Issuer()
        attribute_query.issuer.format = Issuer.X509_SUBJECT
        attribute_query.issuer.value = "/CN=Authorisation Service/O=Site A"    
                        
        attribute_query.subject = Subject()  
        attribute_query.subject.nameID = NameID()
        attribute_query.subject.nameID.format = \
            ESGFSamlNamespaces.NAMEID_FORMAT #@UndefinedVariable
        attribute_query.subject.nameID.value = _cfg['subject']
        xsStringNs = SAMLConstants.XSD_NS+"#"+\
                                        XSStringAttributeValue.TYPE_LOCAL_NAME

        siteAAttribute = Attribute()
        siteAAttribute.name = _cfg['siteAttributeName']
        siteAAttribute.nameFormat = xsStringNs
        
        attribute_query.attributes.append(siteAAttribute) 

        binding = SOAPBinding()
        binding.serialise = AttributeQueryElementTree.toXML
        binding.deserialise = ResponseElementTree.fromXML
        
        self.assertRaises(URLError, binding.send, attribute_query, _cfg['uri'])
             
    def test04AttributeQueryInvalidAttrName(self):
        this_section = 'test04AttributeQueryInvalidAttrName'
        _cfg = self.cfg[this_section]
        
        attribute_query = AttributeQuery()
        attribute_query.version = SAMLVersion(SAMLVersion.VERSION_20)
        attribute_query.id = str(uuid4())
        attribute_query.issueInstant = datetime.utcnow()
        
        attribute_query.issuer = Issuer()
        attribute_query.issuer.format = Issuer.X509_SUBJECT
        attribute_query.issuer.value = "/CN=Authorisation Service/O=Site A"    
                        
        attribute_query.subject = Subject()  
        attribute_query.subject.nameID = NameID()
        attribute_query.subject.nameID.format = \
            ESGFSamlNamespaces.NAMEID_FORMAT #@UndefinedVariable
        attribute_query.subject.nameID.value = _cfg['subject']
        xsStringNs = SAMLConstants.XSD_NS+"#"+\
                                        XSStringAttributeValue.TYPE_LOCAL_NAME

        invalidAttribute = Attribute()
        invalidAttribute.name = "myInvalidAttributeName"
        invalidAttribute.nameFormat = xsStringNs
        
        attribute_query.attributes.append(invalidAttribute) 

        binding = SOAPBinding.fromConfig(self.__class__.CONFIG_FILEPATH, 
                                         prefix='saml.', 
                                         section=this_section)
        
        self.assertRaises(URLError, binding.send, attribute_query, _cfg['uri'])
             
    def test05AttributeQueryWithESGFAttributeType(self):
        # Test interface with custom ESGF Group/Role attribute type
        this_section = 'test05AttributeQueryWithESGFAttributeType'
        _cfg = self.cfg[this_section]
        
        attribute_query = AttributeQuery()
        attribute_query.version = SAMLVersion(SAMLVersion.VERSION_20)
        attribute_query.id = str(uuid4())
        attribute_query.issueInstant = datetime.utcnow()
        
        attribute_query.issuer = Issuer()
        attribute_query.issuer.format = Issuer.X509_SUBJECT
        attribute_query.issuer.value = "/CN=Authorisation Service/O=Site A"    
                        
        attribute_query.subject = Subject()  
        attribute_query.subject.nameID = NameID()
        attribute_query.subject.nameID.format = \
            ESGFSamlNamespaces.NAMEID_FORMAT #@UndefinedVariable
        attribute_query.subject.nameID.value = _cfg['subject']
        
        groupRoleAttribute = Attribute()
        groupRoleAttribute.name = self.__class__.ATTRIBUTE_NAMES[-1]
        groupRoleAttribute.nameFormat = \
            ESGFGroupRoleAttributeValue.TYPE_LOCAL_NAME
        
        attribute_query.attributes.append(groupRoleAttribute) 

        binding = SOAPBinding.fromConfig(self.__class__.CONFIG_FILEPATH, 
                                         prefix='saml.',
                                         section=this_section)
        
        self.assertRaises(URLError, binding.send, attribute_query, _cfg['uri'])
       
    def test06AttributeQuerySOAPBindingInterface(self):
        _cfg = self.cfg['test06AttributeQuerySOAPBindingInterface']
        
        query = AttributeQueryFactory.create()
        
        query.subject.nameID.format = ESGFSamlNamespaces.NAMEID_FORMAT #@UndefinedVariable
        query.subject.nameID.value = self.__class__.OPENID_URI

        query.issuer.value = str(self.__class__.VALID_REQUESTOR_IDS[0])        
        query.issuer.format = Issuer.X509_SUBJECT
        query.attributes = ESGFDefaultQueryAttributes.ATTRIBUTES       

        binding = AttributeQuerySOAPBinding()

        self.assertRaises(URLError, binding.send, query, uri=_cfg['uri'])

    def test07AttributeQueryFromConfig(self):
        this_section = 'test07AttributeQueryFromConfig'
        _cfg = self.cfg[this_section]
        
        query = AttributeQueryFactory.from_config(self.cfg_filepath, 
                                                  section=this_section,
                                                  prefix='attributeQuery.')
        
        binding = AttributeQuerySOAPBinding.fromConfig(self.cfg_filepath, 
                                                  section=this_section,
                                                  prefix='binding.')
        
        self.assertIn("1.2", str(binding.clockSkewTolerance), 
                      'Error parsing clock skew tolerance')
        self.assertRaises(URLError, binding.send, query, uri=_cfg['uri'])
        
    def test08AttributeQuerySslSOAPBindingInterface(self):
        this_section = 'test08AttributeQuerySslSOAPBindingInterface'
        _cfg = self.cfg[this_section]
        
        binding = AttributeQuerySslSOAPBinding.fromConfig(
                                            self.cfg_filepath, 
                                            section=this_section,
                                            prefix='binding.')
        
        query = AttributeQueryFactory.from_config(self.cfg_filepath, 
                                                  section=this_section,
                                                  prefix='attributeQuery.')
        
        self.assertEqual(query.issuer.format, Issuer.UNSPECIFIED, 
                         'Error setting issuer format')
        
        self.assertEqual(binding.sslCtxProxy.sslPriKeyFilePath,
                         os.path.expandvars(
                                '$NDGSEC_TEST_CONFIG_DIR/pki/localhost.key'), 
                         'Error reading private key file path')
        
        self.assertRaises(URLError, binding.send, query, uri=_cfg['uri'])

       
if __name__ == "__main__":
    unittest.main()
