from __future__ import absolute_import

import pytest
import os
import sys
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

prefix = '.'
for i in range(0, 3):
    if os.path.isdir(os.path.join(prefix, 'pycdlib')):
        sys.path.insert(0, prefix)
        break
    else:
        prefix = '../' + prefix

import pycdlib.rockridge

# SP record
def test_rrsprecord_parse_double_initialized():
    sp = pycdlib.rockridge.RRSPRecord()
    sp.parse(b'SP\x07\x01\xbe\xef\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sp.parse(b'SP\x07\x01\xbe\xef\x00')
    assert(str(excinfo.value) == 'SP record already initialized!')

def test_rrsprecord_parse_bad_length():
    sp = pycdlib.rockridge.RRSPRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        sp.parse(b'SP\x06\x01\xbe\xef\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrsprecord_parse_bad_check_byte():
    sp = pycdlib.rockridge.RRSPRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        sp.parse(b'SP\x07\x01\xbf\xef\x00')
    assert(str(excinfo.value) == 'Invalid check bytes on rock ridge extension')

def test_rrsprecord_new_double_initialized():
    sp = pycdlib.rockridge.RRSPRecord()
    sp.new(0)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sp.new(0)
    assert(str(excinfo.value) == 'SP record already initialized!')

def test_rrsprecord_record_not_initialized():
    sp = pycdlib.rockridge.RRSPRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sp.record()
    assert(str(excinfo.value) == 'SP record not yet initialized!')

def test_rrsprecord_record():
    sp = pycdlib.rockridge.RRSPRecord()
    sp.new(0)
    rec = sp.record()
    assert(rec == b'SP\x07\x01\xbe\xef\x00')

def test_rrsprecord_length():
    assert(pycdlib.rockridge.RRSPRecord.length() == 7)

# RR record
def test_rrrrrecord_parse_double_initialized():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.parse(b'RR\x05\x01\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        rr.parse(b'RR\x05\x01\x00')
    assert(str(excinfo.value) == 'RR record already initialized!')

def test_rrrrrecord_parse_bad_length():
    rr = pycdlib.rockridge.RRRRRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        rr.parse(b'RR\x06\x01\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrrrrecord_new_double_initialized():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        rr.new()
    assert(str(excinfo.value) == 'RR record already initialized!')

def test_rrrrrecord_append_field_not_initialized():
    rr = pycdlib.rockridge.RRRRRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        rr.append_field('PX')
    assert(str(excinfo.value) == 'RR record not yet initialized!')

def test_rrrrrecord_append_field_invalid_field():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        rr.append_field('AA')
    assert(str(excinfo.value) == 'Unknown RR field name AA')

def test_rrrrrecord_append_field_px():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('PX')
    assert(rr.rr_flags == 0x1)

def test_rrrrrecord_append_field_pn():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('PN')
    assert(rr.rr_flags == 0x2)

def test_rrrrrecord_append_field_sl():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('SL')
    assert(rr.rr_flags == 0x4)

def test_rrrrrecord_append_field_nm():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('NM')
    assert(rr.rr_flags == 0x8)

def test_rrrrrecord_append_field_cl():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('CL')
    assert(rr.rr_flags == 0x10)

def test_rrrrrecord_append_field_pl():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('PL')
    assert(rr.rr_flags == 0x20)

def test_rrrrrecord_append_field_re():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('RE')
    assert(rr.rr_flags == 0x40)

def test_rrrrrecord_append_field_tf():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rr.append_field('TF')
    assert(rr.rr_flags == 0x80)

def test_rrrrrecord_record_not_initialized():
    rr = pycdlib.rockridge.RRRRRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        rr.record()
    assert(str(excinfo.value) == 'RR record not yet initialized!')

def test_rrrrrecord_record():
    rr = pycdlib.rockridge.RRRRRecord()
    rr.new()
    rec = rr.record()
    assert(rec == b'RR\x05\x01\x00')

def test_rrrrrecord_length():
    assert(pycdlib.rockridge.RRRRRecord.length() == 5)

# CE record
def test_rrcerecord_parse_double_initialized():
    ce = pycdlib.rockridge.RRCERecord()
    ce.parse(b'CE\x1c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        ce.parse(b'CE\x1c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'CE record already initialized!')

def test_rrcerecord_parse_bad_length():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        ce.parse(b'CE\x1a\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrcerecord_parse_bl_le_be_mismatch():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        ce.parse(b'CE\x1c\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'CE record big and little endian continuation area do not agree')

def test_rrcerecord_parse_offset_le_be_mismatch():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        ce.parse(b'CE\x1c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'CE record big and little endian continuation area offset do not agree')

def test_rrcerecord_parse_len_le_be_mismatch():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        ce.parse(b'CE\x1c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'CE record big and little endian continuation area length do not agree')

def test_rrcerecord_new_double_initialized():
    ce = pycdlib.rockridge.RRCERecord()
    ce.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        ce.new()
    assert(str(excinfo.value) == 'CE record already initialized!')

def test_rrcerecord_update_extent_not_initialized():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        ce.update_extent(0)
    assert(str(excinfo.value) == 'CE record not yet initialized!')

def test_rrcerecord_update_offset_not_initialized():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        ce.update_offset(0)
    assert(str(excinfo.value) == 'CE record not yet initialized!')

def test_rrcerecord_update_add_record_not_initialized():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        ce.add_record(0)
    assert(str(excinfo.value) == 'CE record not yet initialized!')

def test_rrcerecord_record_not_initialized():
    ce = pycdlib.rockridge.RRCERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        ce.record()
    assert(str(excinfo.value) == 'CE record not yet initialized!')

def test_rrcerecord_record():
    ce = pycdlib.rockridge.RRCERecord()
    ce.new()
    rec = ce.record()
    assert(rec == b'CE\x1c\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def test_rrcerecord_length():
    assert(pycdlib.rockridge.RRCERecord.length() == 28)

# PX record
def test_rrpxrecord_parse_double_initialized():
    px = pycdlib.rockridge.RRPXRecord()
    px.parse(b'PX\x24\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        px.parse(b'PX\x24\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PX record already initialized!')

def test_rrpxrecord_parse_mode_le_be_mismatch():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        px.parse(b'PX\x24\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PX record big and little-endian file mode do not agree')

def test_rrpxrecord_parse_links_le_be_mismatch():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        px.parse(b'PX\x24\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PX record big and little-endian file links do not agree')

def test_rrpxrecord_parse_user_le_be_mismatch():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        px.parse(b'PX\x24\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PX record big and little-endian file user ID do not agree')

def test_rrpxrecord_parse_group_le_be_mismatch():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        px.parse(b'PX\x24\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PX record big and little-endian file group ID do not agree')

def test_rrpxrecord_parse_serial_le_be_mismatch():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        px.parse(b'PX\x2C\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PX record big and little-endian file serial number do not agree')

def test_rrpxrecord_parse_bad_length():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        px.parse(b'PX\x23\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Invalid length on Rock Ridge PX record')

def test_rrpxrecord_new_double_initialized():
    px = pycdlib.rockridge.RRPXRecord()
    px.new(0)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        px.new(0)
    assert(str(excinfo.value) == 'PX record already initialized!')

def test_rrpxrecord_record_not_initialized():
    px = pycdlib.rockridge.RRPXRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        px.record('1.12')
    assert(str(excinfo.value) == 'PX record not yet initialized!')

def test_rrpxrecord_record_invalid_version():
    px = pycdlib.rockridge.RRPXRecord()
    px.new(0)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        px.record('4.0')
    assert(str(excinfo.value) == 'Invalid rr_version')

def test_rrpxrecord_record():
    px = pycdlib.rockridge.RRPXRecord()
    px.new(0)
    rec = px.record('1.09')
    assert(rec == b'PX\x24\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def test_rrpxrecord_length_oneohnine():
    assert(pycdlib.rockridge.RRPXRecord.length('1.09') == 36)

def test_rrpxrecord_length_onetwelve():
    assert(pycdlib.rockridge.RRPXRecord.length('1.12') == 44)

def test_rrpxrecord_length_invalid_version():
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pycdlib.rockridge.RRPXRecord.length('4.0')
    assert(str(excinfo.value) == 'Invalid rr_version')

# ER record
def test_rrerrecord_parse_double_initialized():
    er = pycdlib.rockridge.RRERRecord()
    er.parse(b'ER\x0b\x01\x01\x01\x01\x01aaa')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        er.parse(b'ER\x0b\x01\x01\x01\x01\x01aaa')
    assert(str(excinfo.value) == 'ER record already initialized!')

def test_rrerrecord_parse_bad_length():
    er = pycdlib.rockridge.RRERRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        er.parse(b'ER\x19\x01\x01\x01\x01\x01aaa')
    assert(str(excinfo.value) == 'Length of ER record much too long')

def test_rrerrecord_parse_len_gt_su_len():
    er = pycdlib.rockridge.RRERRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        er.parse(b'ER\x09\x01\x09\x01\x01\x01aaa')
    assert(str(excinfo.value) == 'Combined length of ER ID, des, and src longer than record')

def test_rrerrecord_new_double_initialized():
    er = pycdlib.rockridge.RRERRecord()
    er.new(b'', b'', b'')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        er.new(b'', b'', b'')
    assert(str(excinfo.value) == 'ER record already initialized!')

def test_rrerrecord_record_not_initialized():
    er = pycdlib.rockridge.RRERRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        er.record()
    assert(str(excinfo.value) == 'ER record not yet initialized!')

def test_rrerrecord_record():
    er = pycdlib.rockridge.RRERRecord()
    er.new(b'a', b'a', b'a')
    rec = er.record()
    assert(rec == b'ER\x0b\x01\x01\x01\x01\x01aaa')

def test_rrerrecord_length():
    assert(pycdlib.rockridge.RRERRecord.length(b'a', b'a', b'a') == 11)

# ES record
def test_rresrecord_parse_double_initialized():
    es = pycdlib.rockridge.RRESRecord()
    es.parse(b'ES\x05\x01\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        es.parse(b'ES\x05\x01\x00')
    assert(str(excinfo.value) == 'ES record already initialized!')

def test_rresrecord_parse_bad_length():
    es = pycdlib.rockridge.RRESRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        es.parse(b'ES\x06\x01\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rresrecord_new_double_initialized():
    es = pycdlib.rockridge.RRESRecord()
    es.new(0)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        es.new(0)
    assert(str(excinfo.value) == 'ES record already initialized!')

def test_rresrecord_record_not_initialized():
    es = pycdlib.rockridge.RRESRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        es.record()
    assert(str(excinfo.value) == 'ES record not yet initialized!')

def test_rresrecord_record():
    es = pycdlib.rockridge.RRESRecord()
    es.new(0)
    rec = es.record()
    assert(rec == b'ES\x05\x01\x00')

def test_rresrecord_length():
    assert(pycdlib.rockridge.RRESRecord.length() == 5)

# PN record
def test_rrpnrecord_parse_double_initialized():
    pn = pycdlib.rockridge.RRPNRecord()
    pn.parse(b'PN\x14\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pn.parse(b'PN\x14\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PN record already initialized!')

def test_rrpnrecord_parse_bad_length():
    pn = pycdlib.rockridge.RRPNRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        pn.parse(b'PN\x13\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrpnrecord_parse_dev_high_be_le_mismatch():
    pn = pycdlib.rockridge.RRPNRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        pn.parse(b'PN\x14\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Dev_t high little-endian does not match big-endian')

def test_rrpnrecord_parse_dev_low_be_le_mismatch():
    pn = pycdlib.rockridge.RRPNRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        pn.parse(b'PN\x14\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Dev_t low little-endian does not match big-endian')

def test_rrpnrecord_new_double_initialized():
    pn = pycdlib.rockridge.RRPNRecord()
    pn.new(0, 0)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pn.new(0, 0)
    assert(str(excinfo.value) == 'PN record already initialized!')

def test_rrpnrecord_record_not_initialized():
    pn = pycdlib.rockridge.RRPNRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pn.record()
    assert(str(excinfo.value) == 'PN record not yet initialized!')

def test_rrpnrecord_record():
    pn = pycdlib.rockridge.RRPNRecord()
    pn.new(0, 0)
    rec = pn.record()
    assert(rec == b'PN\x14\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def test_rrpnrecord_length():
    assert(pycdlib.rockridge.RRPNRecord.length() == 20)

# SL.Component
def test_rrsl_component_bad_flags():
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        com = pycdlib.rockridge.RRSLRecord.Component(0x10, 0, b'')
    assert(str(excinfo.value) == 'Invalid Rock Ridge symlink flags 0x10')

def test_rrsl_component_bad_length():
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        com = pycdlib.rockridge.RRSLRecord.Component(0x02, 1, b'')
    assert(str(excinfo.value) == 'Rock Ridge symlinks to dot, dotdot, or root should have zero length')

def test_rrsl_component_name_dot():
    com = pycdlib.rockridge.RRSLRecord.Component(0x02, 0, b'')
    assert(com.name() == b'.')

def test_rrsl_component_name_dotdot():
    com = pycdlib.rockridge.RRSLRecord.Component(0x04, 0, b'')
    assert(com.name() == b'..')

def test_rrsl_component_name_root():
    com = pycdlib.rockridge.RRSLRecord.Component(0x08, 0, b'')
    assert(com.name() == b'/')

def test_rrsl_component_is_continued():
    com = pycdlib.rockridge.RRSLRecord.Component(0x01, 0, b'')
    assert(com.is_continued())

def test_rrsl_component_record_dot():
    com = pycdlib.rockridge.RRSLRecord.Component(0x02, 0, b'')
    assert(com.record() == b'\x02\x00')

def test_rrsl_component_record_dotdot():
    com = pycdlib.rockridge.RRSLRecord.Component(0x04, 0, b'')
    assert(com.record() == b'\x04\x00')

def test_rrsl_component_record_root():
    com = pycdlib.rockridge.RRSLRecord.Component(0x08, 0, b'')
    assert(com.record() == b'\x08\x00')

def test_rrsl_component_set_continued():
    com = pycdlib.rockridge.RRSLRecord.Component(0x0, 0, b'')
    com.set_continued()
    assert(com.is_continued())

def test_rrsl_component_equal():
    com = pycdlib.rockridge.RRSLRecord.Component(0x0, 0, b'')
    com2 = pycdlib.rockridge.RRSLRecord.Component(0x0, 0, b'')
    assert(com == com2)

def test_rrsl_component_not_equal():
    com = pycdlib.rockridge.RRSLRecord.Component(0x0, 0, b'')
    com2 = pycdlib.rockridge.RRSLRecord.Component(0x1, 0, b'')
    assert(com != com2)

def test_rrsl_component_length_dot():
    assert(pycdlib.rockridge.RRSLRecord.Component.length(b'.') == 2)

def test_rrsl_component_length_dotdot():
    assert(pycdlib.rockridge.RRSLRecord.Component.length(b'..') == 2)

def test_rrsl_component_length_root():
    assert(pycdlib.rockridge.RRSLRecord.Component.length(b'/') == 2)

def test_rrsl_component_length_root():
    assert(pycdlib.rockridge.RRSLRecord.Component.length(b'foo') == 5)

def test_rrsl_component_factory_dot():
    com = pycdlib.rockridge.RRSLRecord.Component.factory(b'.')
    assert(com.flags == 0x2)
    assert(com.curr_length == 0)
    assert(com.data == b'.')

def test_rrsl_component_factory_dotdot():
    com = pycdlib.rockridge.RRSLRecord.Component.factory(b'..')
    assert(com.flags == 0x4)
    assert(com.curr_length == 0)
    assert(com.data == b'..')

def test_rrsl_component_factory_root():
    com = pycdlib.rockridge.RRSLRecord.Component.factory(b'/')
    assert(com.flags == 0x8)
    assert(com.curr_length == 0)
    assert(com.data == b'/')

def test_rrsl_component_factory():
    com = pycdlib.rockridge.RRSLRecord.Component.factory(b'foo')
    assert(com.flags == 0x0)
    assert(com.curr_length == 3)
    assert(com.data == b'foo')

# SL record
def test_rrslrecord_parse_double_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.parse(b'SL\x08\x01\x00\x00\x03foo')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.parse(b'SL\x08\x01\x00\x00\x03foo')
    assert(str(excinfo.value) == 'SL record already initialized!')

def test_rrslrecord_new_double_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.new()
    assert(str(excinfo.value) == 'SL record already initialized!')

def test_rrslrecord_add_component_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.add_component(b'a')
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_add_component_too_long():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput) as excinfo:
        sl.add_component(b'a'*256)
    assert(str(excinfo.value) == 'Symlink would be longer than 255')

def test_rrslrecord_current_length_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.current_length()
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_record_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.record()
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_name_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.name()
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_name_with_root():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.new()
    sl.add_component(b'/')
    assert(sl.name() == b'')

def test_rrslrecord_name_with_continued_comp():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.new()
    sl.add_component(b'foo')
    sl.set_last_component_continued()
    sl.add_component(b'bar')
    assert(sl.name() == b'foobar')

def test_rrslrecord_set_continued_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.set_continued()
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_set_last_component_continued_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.set_last_component_continued()
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_set_last_component_continued_no_components():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.set_last_component_continued()
    assert(str(excinfo.value) == 'Trying to set continued on a non-existent component!')

def test_rrslrecord_last_component_continued_not_initialized():
    sl = pycdlib.rockridge.RRSLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.last_component_continued()
    assert(str(excinfo.value) == 'SL record not yet initialized!')

def test_rrslrecord_last_component_continued_no_components():
    sl = pycdlib.rockridge.RRSLRecord()
    sl.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sl.last_component_continued()
    assert(str(excinfo.value) == 'Trying to get continued on a non-existent component!')

# NM record
def test_rrnmrecord_parse_double_initialized():
    nm = pycdlib.rockridge.RRNMRecord()
    nm.parse(b'NM\x05\x01\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        nm.parse(b'NM\x05\x01\x00')
    assert(str(excinfo.value) == 'NM record already initialized!')

def test_rrnmrecord_parse_invalid_flag():
    nm = pycdlib.rockridge.RRNMRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        nm.parse(b'NM\x05\x01\x03')
    assert(str(excinfo.value) == 'Invalid Rock Ridge NM flags')

def test_rrnmrecord_parse_invalid_flag_with_name():
    nm = pycdlib.rockridge.RRNMRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        nm.parse(b'NM\x06\x01\x02a')
    assert(str(excinfo.value) == 'Invalid name in Rock Ridge NM entry (0x2 1)')

def test_rrnmrecord_new_double_initialized():
    nm = pycdlib.rockridge.RRNMRecord()
    nm.new(b'foo')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        nm.new(b'foo')
    assert(str(excinfo.value) == 'NM record already initialized!')

def test_rrnmrecord_record_not_initialized():
    nm = pycdlib.rockridge.RRNMRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        nm.record()
    assert(str(excinfo.value) == 'NM record not yet initialized!')

def test_rrnmrecord_set_continued_not_initialized():
    nm = pycdlib.rockridge.RRNMRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        nm.set_continued()
    assert(str(excinfo.value) == 'NM record not yet initialized!')

# CL record
def test_rrclrecord_parse_double_initialized():
    cl = pycdlib.rockridge.RRCLRecord()
    cl.parse(b'CL\x0c\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        cl.parse(b'CL\x0c\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'CL record already initialized!')

def test_rrclrecord_parse_invalid_size():
    cl = pycdlib.rockridge.RRCLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        cl.parse(b'CL\x0d\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrclrecord_parse_be_le_mismatch():
    cl = pycdlib.rockridge.RRCLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        cl.parse(b'CL\x0c\x01\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Little endian block num does not equal big endian; corrupt ISO')

def test_rrclrecord_new_double_initialized():
    cl = pycdlib.rockridge.RRCLRecord()
    cl.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        cl.new()
    assert(str(excinfo.value) == 'CL record already initialized!')

def test_rrclrecord_record_not_initialized():
    cl = pycdlib.rockridge.RRCLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        cl.record()
    assert(str(excinfo.value) == 'CL record not yet initialized!')

def test_rrclrecord_set_log_block_num_not_initialized():
    cl = pycdlib.rockridge.RRCLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        cl.set_log_block_num(0)
    assert(str(excinfo.value) == 'CL record not yet initialized!')

# PL record
def test_rrplrecord_parse_double_initialized():
    pl = pycdlib.rockridge.RRPLRecord()
    pl.parse(b'PL\x0c\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pl.parse(b'PL\x0c\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'PL record already initialized!')

def test_rrplrecord_parse_invalid_size():
    pl = pycdlib.rockridge.RRPLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        pl.parse(b'PL\x0d\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrplrecord_parse_be_le_mismatch():
    pl = pycdlib.rockridge.RRPLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        pl.parse(b'PL\x0c\x01\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Little endian block num does not equal big endian; corrupt ISO')

def test_rrplrecord_new_double_initialized():
    pl = pycdlib.rockridge.RRPLRecord()
    pl.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pl.new()
    assert(str(excinfo.value) == 'PL record already initialized!')

def test_rrplrecord_record_not_initialized():
    pl = pycdlib.rockridge.RRPLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pl.record()
    assert(str(excinfo.value) == 'PL record not yet initialized!')

def test_rrplrecord_set_log_block_num_not_initialized():
    pl = pycdlib.rockridge.RRPLRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pl.set_log_block_num(0)
    assert(str(excinfo.value) == 'PL record not yet initialized!')

# TF record
def test_rrtfrecord_parse_double_initialized():
    tf = pycdlib.rockridge.RRTFRecord()
    tf.parse(b'TF\x05\x01\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        tf.parse(b'TF\x05\x01\x00')
    assert(str(excinfo.value) == 'TF record already initialized!')

def test_rrtfrecord_parse_invalid_size():
    tf = pycdlib.rockridge.RRTFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        tf.parse(b'TF\x04\x01\x00')
    assert(str(excinfo.value) == 'Not enough bytes in the TF record')

def test_rrtfrecord_parse_use_vol_desc_dates():
    tf = pycdlib.rockridge.RRTFRecord()
    tf.parse(b'TF\x16\x01\x81' + b'\x00'*17)
    assert(tf.creation_time.date_str == b'0' * 16 + b'\x00')

def test_rrtfrecord_new_double_initialized():
    tf = pycdlib.rockridge.RRTFRecord()
    tf.new(0)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        tf.new(0)
    assert(str(excinfo.value) == 'TF record already initialized!')

def test_rrtfrecord_new_use_vol_desc_dates():
    tf = pycdlib.rockridge.RRTFRecord()
    tf.new(0x81)
    assert(tf.creation_time.date_str == b'0' * 16 + b'\x00')

def test_rrtfrecord_record_not_initialized():
    tf = pycdlib.rockridge.RRTFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        tf.record()
    assert(str(excinfo.value) == 'TF record not yet initialized!')

def test_rrtfrecord_length_use_vol_desc_dates():
    assert(pycdlib.rockridge.RRTFRecord.length(0x81) == 0x16)

# SF record
def test_rrsfrecord_parse_double_initialized():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.parse(b'SF\x0C\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sf.parse(b'SF\x0C\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'SF record already initialized!')

def test_rrsfrecord_parse_one_ten():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.parse(b'SF\x0C\x01\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(sf.virtual_file_size_low == 0)

def test_rrsfrecord_parse_one_ten_be_le_mismatch():
    sf = pycdlib.rockridge.RRSFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        sf.parse(b'SF\x0C\x01\x00\x00\x00\x01\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Virtual file size little-endian does not match big-endian')

def test_rrsfrecord_parse_one_twelve_high_be_le_mismatch():
    sf = pycdlib.rockridge.RRSFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        sf.parse(b'SF\x15\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Virtual file size high little-endian does not match big-endian')

def test_rrsfrecord_parse_one_twelve_low_be_le_mismatch():
    sf = pycdlib.rockridge.RRSFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        sf.parse(b'SF\x15\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Virtual file size low little-endian does not match big-endian')

def test_rrsfrecord_parse_one_twelve():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.parse(b'SF\x15\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(sf.virtual_file_size_low == 0)
    assert(sf.virtual_file_size_high == 0)
    assert(sf.table_depth == 0)

def test_rrsfrecord_parse_invalid_length():
    sf = pycdlib.rockridge.RRSFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        sf.parse(b'SF\x16\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert(str(excinfo.value) == 'Invalid length on Rock Ridge SF record (expected 12 or 21)')

def test_rrsfrecord_new_double_initialized():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.new(None, 0, None)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sf.new(None, 0, None)
    assert(str(excinfo.value) == 'SF record already initialized!')

def test_rrsfrecord_new_one_ten():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.new(None, 0, None)
    assert(sf.virtual_file_size_low == 0)

def test_rrsfrecord_new_one_twelve():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.new(0, 0, 0)
    assert(sf.virtual_file_size_low == 0)
    assert(sf.virtual_file_size_high == 0)
    assert(sf.table_depth == 0)

def test_rrsfrecord_record_not_initialized():
    sf = pycdlib.rockridge.RRSFRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        sf.record()
    assert(str(excinfo.value) == 'SF record not yet initialized!')

def test_rrsfrecord_record_one_ten():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.new(None, 0, None)
    assert(sf.record() == b'SF\x0C\x01\x00\x00\x00\x00\x00\x00\x00\x00')

def test_rrsfrecord_record_one_twelve():
    sf = pycdlib.rockridge.RRSFRecord()
    sf.new(0, 0, 0)
    assert(sf.record() == b'SF\x15\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def test_rrsfrecord_length_one_ten():
    assert(pycdlib.rockridge.RRSFRecord.length('1.10') == 12)

def test_rrsfrecord_length_one_twelve():
    assert(pycdlib.rockridge.RRSFRecord.length('1.12') == 21)

def test_rrsfrecord_length_invalid_version():
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pycdlib.rockridge.RRSFRecord.length('foo')
    assert(str(excinfo.value) == 'Invalid rr_version')

# RE record
def test_rrrerecord_parse_double_initialized():
    re = pycdlib.rockridge.RRRERecord()
    re.parse(b'RE\x04\x01')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        re.parse(b'RE\x04\x01')
    assert(str(excinfo.value) == 'RE record already initialized!')

def test_rrrerecord_parse_bad_length():
    re = pycdlib.rockridge.RRRERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        re.parse(b'RE\x06\x01\xbe\xef\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrrerecord_new_double_initialized():
    re = pycdlib.rockridge.RRRERecord()
    re.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        re.new()
    assert(str(excinfo.value) == 'RE record already initialized!')

def test_rrrerecord_record_not_initialized():
    re = pycdlib.rockridge.RRRERecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        re.record()
    assert(str(excinfo.value) == 'RE record not yet initialized!')

def test_rrrerecord_record():
    re = pycdlib.rockridge.RRRERecord()
    re.new()
    assert(re.record() == b'RE\x04\x01')

def test_rrrerecord_length():
    assert(pycdlib.rockridge.RRRERecord.length() == 4)

# ST record
def test_rrstrecord_parse_double_initialized():
    st = pycdlib.rockridge.RRSTRecord()
    st.parse(b'ST\x04\x01')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        st.parse(b'ST\x04\x01')
    assert(str(excinfo.value) == 'ST record already initialized!')

def test_rrstrecord_parse_bad_length():
    st = pycdlib.rockridge.RRSTRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        st.parse(b'ST\x06\x01\xbe\xef\x00')
    assert(str(excinfo.value) == 'Invalid length on rock ridge extension')

def test_rrstrecord_new_double_initialized():
    st = pycdlib.rockridge.RRSTRecord()
    st.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        st.new()
    assert(str(excinfo.value) == 'ST record already initialized!')

def test_rrstrecord_record_not_initialized():
    st = pycdlib.rockridge.RRSTRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        st.record()
    assert(str(excinfo.value) == 'ST record not yet initialized!')

def test_rrstrecord_record():
    st = pycdlib.rockridge.RRSTRecord()
    st.new()
    assert(st.record() == b'ST\x04\x01')

def test_rrstrecord_length():
    assert(pycdlib.rockridge.RRSTRecord.length() == 4)

# PD record
def test_rrpdrecord_parse_double_initialized():
    pd = pycdlib.rockridge.RRPDRecord()
    pd.parse(b'PD\x04\x01\x00')
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pd.parse(b'PD\x04\x01\x00')
    assert(str(excinfo.value) == 'PD record already initialized!')

def test_rrpdrecord_new_double_initialized():
    pd = pycdlib.rockridge.RRPDRecord()
    pd.new()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pd.new()
    assert(str(excinfo.value) == 'PD record already initialized!')

def test_rrpdrecord_record_not_initialized():
    pd = pycdlib.rockridge.RRPDRecord()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInternalError) as excinfo:
        pd.record()
    assert(str(excinfo.value) == 'PD record not yet initialized!')

def test_rrpdrecord_record():
    pd = pycdlib.rockridge.RRPDRecord()
    pd.new()
    assert(pd.record() == b'PD\x04\x01')

def test_rrpdrecord_length():
    assert(pycdlib.rockridge.RRPDRecord.length(b'') == 4)

# RockRidgeContinuationBlock and RockRidgeContinuationEntry
def test_rrcontentry_track_into_empty():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(0, 23)

    assert(len(rr._entries) == 1)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)

def test_rrcontentry_track_at_end():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(0, 23)
    rr.track_entry(23, 33)

    assert(len(rr._entries) == 2)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)
    assert(rr._entries[1].offset == 23)
    assert(rr._entries[1].length == 33)

def test_rrcontentry_track_at_beginning():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(23, 33)
    rr.track_entry(0, 23)

    assert(len(rr._entries) == 2)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)
    assert(rr._entries[1].offset == 23)
    assert(rr._entries[1].length == 33)

def test_rrcontentry_track_overlap():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(0, 23)

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        rr.track_entry(22, 33)
    assert(str(excinfo.value) == 'Overlapping CE regions on the ISO')

def test_rrcontentry_track_rest():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(0, 23)
    rr.track_entry(23, 2025)

    assert(len(rr._entries) == 2)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)
    assert(rr._entries[1].offset == 23)
    assert(rr._entries[1].length == 2025)

def test_rrcontentry_track_toolarge():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(0, 23)

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO) as excinfo:
        rr.track_entry(23, 2026)
    assert(str(excinfo.value) == 'No room in continuation block to track entry')

def test_rrcontentry_add_into_empty():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    assert(rr.add_entry(23) is not None)

    assert(len(rr._entries) == 1)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)

def test_rrcontentry_add_at_end():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    assert(rr.add_entry(23) is not None)
    assert(rr.add_entry(33) is not None)

    assert(len(rr._entries) == 2)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)
    assert(rr._entries[1].offset == 23)
    assert(rr._entries[1].length == 33)

def test_rrcontentry_add_at_beginning():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    rr.track_entry(23, 33)
    assert(rr.add_entry(23) is not None)

    assert(len(rr._entries) == 2)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)
    assert(rr._entries[1].offset == 23)
    assert(rr._entries[1].length == 33)

def test_rrcontentry_add_multiple():
    rr = pycdlib.rockridge.RockRidgeContinuationBlock(24, 2048)
    assert(rr.add_entry(23) is not None)
    rr.track_entry(40, 12)
    assert(rr.add_entry(12) is not None)

    assert(len(rr._entries) == 3)
    assert(rr._entries[0].offset == 0)
    assert(rr._entries[0].length == 23)
    assert(rr._entries[1].offset == 23)
    assert(rr._entries[1].length == 12)
    assert(rr._entries[2].offset == 40)
    assert(rr._entries[2].length == 12)
