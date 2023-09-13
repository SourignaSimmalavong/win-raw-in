import re
from dataclasses import dataclass
from typing import Optional

GUID = {
    'BUS1394_CLASS_GUID': "6BDD1FC1-810F-11d0-BEC7-08002BE2092F",
    '61883_CLASS': "7EBEFBC0-3200-11d2-B4C2-00A0C9697D07",
    'APPLICATIONLAUNCH_BUTTON': "629758EE-986E-4D9E-8E47-DE27F8AB054D",
    'BATTERY': "72631E54-78A4-11D0-BCF7-00AA00B7B32A",
    'LID': "4AFA3D52-74A7-11d0-be5e-00A0C9062857",
    'MEMORY': "3FD0F03D-92E0-45FB-B75C-5ED8FFB01021",
    'MESSAGE_INDICATOR': "CD48A365-FA94-4CE2-A232-A1B764E5D8B4",
    'PROCESSOR': "97FADB10-4E33-40AE-359C-8BEF029DBDD0",
    'SYS_BUTTON': "4AFA3D53-74A7-11d0-be5e-00A0C9062857",
    'THERMAL_ZONE': "4AFA3D51-74A7-11d0-be5e-00A0C9062857",
    'BTHPORT_DEVICE_INTERFACE': "0850302A-B344-4fda-9BE9-90576B8D46F0",
    'BRIGHTNESS': "FDE5BBA4-B3F9-46FB-BDAA-0728CE3100B4",
    'DISPLAY_ADAPTER': "5B45201D-F2F2-4F3B-85BB-30FF1F953599",
    'I2C': "2564AA4F-DDDB-4495-B497-6AD4A84163D7",
    'IMAGE': "6BDD1FC6-810F-11D0-BEC7-08002BE2092F",
    'MONITOR': "E6F07B5F-EE97-4a90-B076-33F57BF4EAA7",
    'OPM': "BF4672DE-6B4E-4BE4-A325-68A91EA49C09",
    'VIDEO_OUTPUT_ARRIVAL': "1AD9E4F0-F88D-4360-BAB9-4C2D55E564CD",
    'DISPLAY_DEVICE_ARRIVAL': "1CA05180-A699-450A-9A0C-DE4FBE3DDD89",
    'HID': "4D1E55B2-F16F-11CF-88CB-001111000030",
    'KEYBOARD': "884b96c3-56ef-11d1-bc8c-00a0c91405dd",
    'MOUSE': "378DE44C-56EF-11D1-BC8C-00A0C91405DD",
    'MODEM': "2C7089AA-2E0E-11D1-B114-00C04FC2AAE4",
    'NET': "CAC88484-7515-4C03-82E6-71A87ABAC361",
    'SENSOR': "BA1BB692-9B7A-4833-9A1E-525ED134E7E2",
    'COMPORT': "86E0D1E0-8089-11D0-9CE4-08003E301F73",
    'PARALLEL': "97F76EF0-F883-11D0-AF1F-0000F800845C",
    'PARCLASS': "811FC6A5-F728-11D0-A537-0000F8753ED1",
    'SERENUM_BUS_ENUMERATOR': "4D36E978-E325-11CE-BFC1-08002BE10318",
    'CDCHANGER': "53F56312-B6BF-11D0-94F2-00A0C91EFB8B",
    'CDROM': "53F56308-B6BF-11D0-94F2-00A0C91EFB8B",
    'DISK': "53F56307-B6BF-11D0-94F2-00A0C91EFB8B",
    'FLOPPY': "53F56311-B6BF-11D0-94F2-00A0C91EFB8B",
    'MEDIUMCHANGER': "53F56310-B6BF-11D0-94F2-00A0C91EFB8B",
    'PARTITION': "53F5630A-B6BF-11D0-94F2-00A0C91EFB8B",
    'STORAGEPORT': "2ACCFE60-C130-11D2-B082-00A0C91EFB8B",
    'TAPE': "53F5630B-B6BF-11D0-94F2-00A0C91EFB8B",
    'VOLUME': "53F5630D-B6BF-11D0-94F2-00A0C91EFB8B",
    'WRITEONCEDISK': "53F5630C-B6BF-11D0-94F2-00A0C91EFB8B",
    'IO_VOLUME_DEVICE_INTERFACE': "53F5630D-B6BF-11D0-94F2-00A0C91EFB8B",
    'MOUNTDEV_MOUNTED_DEVICE_GUID': "53F5630D-B6BF-11D0-94F2-00A0C91EFB8B",
    'AVC_CLASS': "095780C3-48A1-4570-BD95-46707F78C2DC",
    'VIRTUAL_AVC_CLASS': "616EF4D0-23CE-446D-A568-C31EB01913D0",
    'KS_ACOUSTIC_ECHO_CANCEL': "BF963D80-C559-11D0-8A2B-00A0C9255AC1",
    'KS_AUDIO': "6994AD04-93EF-11D0-A3CC-00A0C9223196",
    'KS_AUDIO_DEVICE': "FBF6F530-07B9-11D2-A71E-0000F8004788",
    'KS_AUDIO_GFX': "9BAF9572-340C-11D3-ABDC-00A0C90AB16F",
    'KS_AUDIO_SPLITTER': "9EA331FA-B91B-45F8-9285-BD2BC77AFCDE",
    'KS_BDA_IP_SINK': "71985F4A-1CA1-11d3-9CC8-00C04F7971E0",
    'KS_BDA_NETWORK_EPG': "71985F49-1CA1-11d3-9CC8-00C04F7971E0",
    'KS_BDA_NETWORK_PROVIDER': "71985F4B-1CA1-11d3-9CC8-00C04F7971E0",
    'KS_BDA_NETWORK_TUNER': "71985F48-1CA1-11d3-9CC8-00C04F7971E0",
    'KS_BDA_RECEIVER_COMPONENT': "FD0A5AF4-B41D-11d2-9C95-00C04F7971E0",
    'KS_BDA_TRANSPORT_INFORMATION': "A2E3074F-6C3D-11d3-B653-00C04F79498E",
    'KS_BRIDGE': "085AFF00-62CE-11CF-A5D6-28DB04C10000",
    'KS_CAPTURE': "65E8773D-8F56-11D0-A3B9-00A0C9223196",
    'KS_CLOCK': "53172480-4791-11D0-A5D6-28DB04C10000",
    'KS_COMMUNICATIONSTRANSFORM': "CF1DDA2C-9743-11D0-A3EE-00A0C9223196",
    'KS_CROSSBAR': "A799A801-A46D-11D0-A18C-00A02401DCD4",
    'KS_DATACOMPRESSOR': "1E84C900-7E70-11D0-A5D6-28DB04C10000",
    'KS_DATADECOMPRESSOR': "2721AE20-7E70-11D0-A5D6-28DB04C10000",
    'KS_DATATRANSFORM': "2EB07EA0-7E70-11D0-A5D6-28DB04C10000",
    'KS_DRM_DESCRAMBLE': "FFBB6E3F-CCFE-4D84-90D9-421418B03A8E",
    'KS_ENCODER': "19689BF6-C384-48fd-AD51-90E58C79F70B",
    'KS_ESCALANTE_PLATFORM_DRIVER': "74F3AEA8-9768-11D1-8E07-00A0C95EC22E",
    'KS_FILESYSTEM': "760FED5E-9357-11D0-A3CC-00A0C9223196",
    'KS_INTERFACETRANSFORM': "CF1DDA2D-9743-11D0-A3EE-00A0C9223196",
    'KS_MEDIUMTRANSFORM': "CF1DDA2E-9743-11D0-A3EE-00A0C9223196",
    'KS_MICROPHONE_ARRAY_PROCESSOR': "830A44F2-A32D-476B-BE97-42845673B35A",
    'KS_MIXER': "AD809C00-7B88-11D0-A5D6-28DB04C10000",
    'KS_MULTIPLEXER': "7A5DE1D3-01A1-452c-B481-4FA2B96271E8",
    'KS_NETWORK': "67C9CC3C-69C4-11D2-8759-00A0C9223196",
    'KS_PREFERRED_MIDIOUT_DEVICE': "D6C50674-72C1-11D2-9755-0000F8004788",
    'KS_PREFERRED_WAVEIN_DEVICE': "D6C50671-72C1-11D2-9755-0000F8004788",
    'KS_PREFERRED_WAVEOUT_DEVICE': "D6C5066E-72C1-11D2-9755-0000F8004788",
    'KS_PROXY': "97EBAACA-95BD-11D0-A3EA-00A0C9223196",
    'KS_QUALITY': "97EBAACB-95BD-11D0-A3EA-00A0C9223196",
    'KS_REALTIME': "EB115FFC-10C8-4964-831D-6DCB02E6F23F",
    'KS_RENDER': "65E8773E-8F56-11D0-A3B9-00A0C9223196",
    'KS_SPLITTER': "0A4252A0-7E70-11D0-A5D6-28DB04C10000",
    'KS_SYNTHESIZER': "DFF220F3-F70F-11D0-B917-00A0C9223196",
    'KS_SYSAUDIO': "A7C7A5B1-5AF3-11D1-9CED-00A024BF0407",
    'KS_TEXT': "6994AD06-93EF-11D0-A3CC-00A0C9223196",
    'KS_TOPOLOGY': "DDA54A40-1E4C-11D1-A050-405705C10000",
    'KS_TVAUDIO': "A799A802-A46D-11D0-A18C-00A02401DCD4",
    'KS_TVTUNER': "A799A800-A46D-11D0-A18C-00A02401DCD4",
    'KS_VBICODEC': "07DAD660-22F1-11D1-A9F4-00C04FBBDE8F",
    'KS_VIDEO': "6994AD05-93EF-11D0-A3CC-00A0C9223196",
    'KS_VIRTUAL': "3503EAC4-1F26-11D1-8AB0-00A0C9223196",
    'KS_VPMUX': "A799A803-A46D-11D0-A18C-00A02401DCD4",
    'KS_WDMAUD': "3E227E76-690D-11D2-8161-0000F8775BF1",
    'KSMFT_AUDIO_DECODER': "9ea73fb4-ef7a-4559-8d5d-719d8f0426c7",
    'KSMFT_AUDIO_EFFECT': "11064c48-3648-4ed0-932e-05ce8ac811b7",
    'KSMFT_AUDIO_ENCODER': "91c64bd0-f91e-4d8c-9276-db248279d975",
    'KSMFT_DEMULTIPLEXER': "a8700a7a-939b-44c5-99d7-76226b23b3f1",
    'KSMFT_MULTIPLEXER': "059c561e-05ae-4b61-b69d-55b61ee54a7b",
    'KSMFT_OTHER': "90175d57-b7ea-4901-aeb3-933a8747756f",
    'KSMFT_VIDEO_DECODER': "d6c02d4b-6833-45b4-971a-05a4b04bab91",
    'KSMFT_VIDEO_EFFECT': "12e17c21-532c-4a6e-8a1c-40825a736397",
    'KSMFT_VIDEO_ENCODER': "f79eac7d-e545-4387-bdee-d647d7bde42a",
    'KSMFT_VIDEO_PROCESSOR': "302ea3fc-aa5f-47f9-9f7a-c2188bb16302",
    'USB_DEVICE': "A5DCBF10-6530-11D2-901F-00C04FB951ED",
    'USB_HOST_CONTROLLER': "3ABF6F2D-71C4-462A-8A92-1E6861E6AF27",
    'USB_HUB': "F18A0E88-C30C-11D0-8815-00A0C906BED8",
    'WPD': "6AC27878-A6FA-4155-BA85-F98F491D4F33",
    'WPD_PRIVATE': "BA0C718F-4DED-49B7-BDD3-FABE28661211",
    'SIDESHOW': "152E5811-FEB9-4B00-90F4-D32947AE1681",
}
BLUETOOTH_GUID_LOOKUP = {  # from
    "00001800-0000-1000-8000-00805f9b34fb": "Generic Access",
    "00001801-0000-1000-8000-00805f9b34fb": "Generic Attribute",
    "00001802-0000-1000-8000-00805f9b34fb": "Immediate Alert",
    "00001803-0000-1000-8000-00805f9b34fb": "Link Loss",
    "00001804-0000-1000-8000-00805f9b34fb": "Tx Power",
    "00001805-0000-1000-8000-00805f9b34fb": "Current Time Service",
    "00001806-0000-1000-8000-00805f9b34fb": "Reference Time Update Service",
    "00001807-0000-1000-8000-00805f9b34fb": "Next DST Change Service",
    "00001808-0000-1000-8000-00805f9b34fb": "Glucose",
    "00001809-0000-1000-8000-00805f9b34fb": "Health Thermometer",
    "0000180a-0000-1000-8000-00805f9b34fb": "Device Information",
    "0000180d-0000-1000-8000-00805f9b34fb": "Heart Rate",
    "0000180e-0000-1000-8000-00805f9b34fb": "Phone Alert Status Service",
    "0000180f-0000-1000-8000-00805f9b34fb": "Battery Service",
    "00001810-0000-1000-8000-00805f9b34fb": "Blood Pressure",
    "00001811-0000-1000-8000-00805f9b34fb": "Alert Notification Service",
    "00001812-0000-1000-8000-00805f9b34fb": "Human Interface Device",
    "00001813-0000-1000-8000-00805f9b34fb": "Scan Parameters",
    "00001814-0000-1000-8000-00805f9b34fb": "Running Speed and Cadence",
    "00001815-0000-1000-8000-00805f9b34fb": "Automation IO",
    "00001816-0000-1000-8000-00805f9b34fb": "Cycling Speed and Cadence",
    "00001818-0000-1000-8000-00805f9b34fb": "Cycling Power",
    "00001819-0000-1000-8000-00805f9b34fb": "Location and Navigation",
    "0000181a-0000-1000-8000-00805f9b34fb": "Environmental Sensing",
    "0000181b-0000-1000-8000-00805f9b34fb": "Body Composition",
    "0000181c-0000-1000-8000-00805f9b34fb": "User Data",
    "0000181d-0000-1000-8000-00805f9b34fb": "Weight Scale",
    "0000181e-0000-1000-8000-00805f9b34fb": "Bond Management Service",
    "0000181f-0000-1000-8000-00805f9b34fb": "Continuous Glucose Monitoring",
    "00001820-0000-1000-8000-00805f9b34fb": "Internet Protocol Support Service",
    "00001821-0000-1000-8000-00805f9b34fb": "Indoor Positioning",
    "00001822-0000-1000-8000-00805f9b34fb": "Pulse Oximeter Service",
    "00001823-0000-1000-8000-00805f9b34fb": "HTTP Proxy",
    "00001824-0000-1000-8000-00805f9b34fb": "Transport Discovery",
    "00001825-0000-1000-8000-00805f9b34fb": "Object Transfer Service",
    "00001826-0000-1000-8000-00805f9b34fb": "Fitness Machine",
    "00001827-0000-1000-8000-00805f9b34fb": "Mesh Provisioning Service",
    "00001828-0000-1000-8000-00805f9b34fb": "Mesh Proxy Service",
    "00001829-0000-1000-8000-00805f9b34fb": "Reconnection Configuration",
    "00001101-0000-1000-8000-00805F9B34FB": "COM Port",
}


def readable_name(guid_name: str):
    return guid_name.replace("KSMFT_", "").replace("KS_", "").lower().replace("_", " ")


GUID_LOOKUP = {key.lower(): readable_name(name) for name, key in GUID.items()}
GUID_LOOKUP.update({key.lower(): f"Bluetooth {name}" for key, name in BLUETOOTH_GUID_LOOKUP.items()})


@dataclass
class DeviceID:
    category: str
    vendor_id: Optional[int]
    product_id: Optional[int]
    guid: str
    interface_name: Optional[str]


def parse_device_id(device_id: str) -> DeviceID:
    if device_id.startswith('\\\\?\\'):
        category = re.search(r'\\\\\?\\(.*?)[#\\]', device_id).group(1)
    else:
        category = device_id[:device_id.index('\\')]
    if '{' in device_id:
        guid = re.search(r'{(.*?)}', device_id).group(1)
        guid_name = GUID_LOOKUP.get(guid.lower(), None)
    else:
        guid = None
        guid_name = category
    if 'VID_' in device_id:
        vendor_id = re.search(r'VID_(.*?)[&#]', device_id).group(1)
    elif 'VID&' in device_id:
        vendor_id = re.search(r'VID&(.*?)_', device_id).group(1)
    else:
        vendor_id = None
    if 'PID_' in device_id:
        product_id = re.search(r'PID_(.*?)[&#]', device_id).group(1)
    elif 'PID&' in device_id:
        product_id = re.search(r'PID&(.*?)_', device_id).group(1)
    else:
        product_id = None
    # interface_id = re.search(r'MI_(.*?)[&#]', device_id).group(1)
    # collection_id = re.search(r'Col_(.*?)[&#]', device_id).group(1)
    vendor_id = int(vendor_id, 16) if vendor_id is not None else None
    product_id = int(product_id, 16) if product_id is not None else None
    return DeviceID(category, vendor_id, product_id, guid, guid_name)


if __name__ == '__main__':
    # for name in GUID:
    #     print(readable_name(name))
    print(parse_device_id('\\\\?\\HID#{00001812-0000-1000-8000-00805f9b34fb}&Dev&VID_045e&PID_0b13&REV_0509&0c352633ee04&IG_00#a&3724ae32&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}'))
    print(parse_device_id('\\\\?\\ACPI#HPQ8001#4&1e96045d&0#{884b96c3-56ef-11d1-bc8c-00a0c91405dd}'))
    print(parse_device_id('\\\\?\\HID#SYNA329A&Col04#5&fe9eeb2&0&0003#{4d1e55b2-f16f-11cf-88cb-001111000030}'))
    print(parse_device_id(r'BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG&0000\7&B66845&1&000000000000_00000004'))
