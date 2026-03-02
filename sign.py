from signer import md5, ladon, argus, gorgon
from time import time
from random import choice

def generate_signatures(params, data=None, device_id='', aid=1233, license_id=1611921764, 
                       sdk_version_str='v04.04.05-ov-android', sdk_version=134744640, 
                       platform=0, cookie=''):
    x_ss_stub = md5(data.encode()).hexdigest() if data else None
    ticket = time()
    unix = int(ticket)
    
    if not device_id:
        trace = (
            str("%x" % (round(ticket * 1000) & 0xffffffff))
            + "10"
            + "".join(choice('0123456789abcdef') for _ in range(16))
        )
    else:
        trace = (
            hex(int(device_id))[2:]
            + "".join(choice('0123456789abcdef') for _ in range(2))
            + "0"
            + hex(int(aid))[2:]
        )

    return {
        'x-argus': argus.Argus.get_sign(
            params, x_ss_stub, unix,
            platform=platform,
            aid=aid,
            license_id=license_id,
            sec_device_id=device_id,
            sdk_version=sdk_version_str,
            sdk_version_int=sdk_version
        ),
        'x-ladon': ladon.Ladon.encrypt(unix, license_id, aid),
        'x-gorgon': gorgon.get_xgorgon(
            params=params, ticket=ticket, data=data if data else "", cookie=cookie
        ),
        'x-khronos': str(unix),
        'x-ss-req-ticket': str(time()).replace(".", "")[:13],
        'x-tt-trace-id': f"00-{trace}-{trace[:16]}-01",
        'x-ss-stub': x_ss_stub.upper() if data else None
    }