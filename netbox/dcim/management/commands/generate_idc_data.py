"""
IDC 운영 시뮬레이션용 더미 데이터 생성 명령어

사용법:
    python manage.py generate_idc_data
    python manage.py generate_idc_data --clear  # 기존 데이터 삭제 후 생성
"""

import random
from django.core.management.base import BaseCommand
from django.db import transaction

from dcim.models import (
    Site, Location, Manufacturer, DeviceType, DeviceRole,
    Rack, Device, Interface, ConsolePort, PowerPort
)
from dcim.choices import DeviceStatusChoices, SiteStatusChoices, RackStatusChoices
from ipam.models import IPAddress, Prefix, VLAN, VLANGroup
from tenancy.models import Tenant, TenantGroup


class Command(BaseCommand):
    help = 'IDC 운영 시뮬레이션을 위한 더미 데이터 생성'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='기존 더미 데이터를 삭제하고 새로 생성',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('기존 데이터 삭제 중...')
            self.clear_data()

        with transaction.atomic():
            self.stdout.write('IDC 더미 데이터 생성 시작...')

            # 1. 기본 데이터 생성
            tenants = self.create_tenants()
            manufacturers = self.create_manufacturers()
            device_types = self.create_device_types(manufacturers)
            device_roles = self.create_device_roles()

            # 2. 사이트 및 위치 생성
            site = self.create_site()
            locations = self.create_locations(site)

            # 3. 랙 생성
            racks = self.create_racks(locations)

            # 4. VLAN 및 IP 대역 생성
            vlan_group = self.create_vlans(site)
            prefixes = self.create_prefixes(site)

            # 5. 장비 생성 (현황에 맞게)
            devices = self.create_devices(
                locations, racks, device_types, device_roles, tenants
            )

            # 6. IP 주소 할당
            self.assign_ip_addresses(devices, prefixes)

            self.stdout.write(self.style.SUCCESS(
                f'더미 데이터 생성 완료! 총 {len(devices)}대 장비 생성'
            ))

    def clear_data(self):
        """기존 더미 데이터 삭제"""
        # 의존성 순서대로 삭제
        IPAddress.objects.filter(description__contains='[IDC-DUMMY]').delete()
        Device.objects.filter(comments__contains='[IDC-DUMMY]').delete()
        Rack.objects.filter(comments__contains='[IDC-DUMMY]').delete()
        Prefix.objects.filter(description__contains='[IDC-DUMMY]').delete()
        VLAN.objects.filter(description__contains='[IDC-DUMMY]').delete()
        VLANGroup.objects.filter(description__contains='[IDC-DUMMY]').delete()
        Location.objects.filter(description__contains='[IDC-DUMMY]').delete()
        Site.objects.filter(comments__contains='[IDC-DUMMY]').delete()
        DeviceRole.objects.filter(description__contains='[IDC-DUMMY]').delete()
        DeviceType.objects.filter(comments__contains='[IDC-DUMMY]').delete()
        Manufacturer.objects.filter(description__contains='[IDC-DUMMY]').delete()
        Tenant.objects.filter(comments__contains='[IDC-DUMMY]').delete()
        TenantGroup.objects.filter(description__contains='[IDC-DUMMY]').delete()

    def create_tenants(self):
        """테넌트(부서) 생성"""
        self.stdout.write('  테넌트 생성 중...')

        # 테넌트 그룹
        group, _ = TenantGroup.objects.get_or_create(
            name='본부',
            slug='division',
            defaults={'description': '[IDC-DUMMY] 본부 그룹'}
        )

        tenant_data = [
            ('인프라운영팀', 'infra-ops', '인프라 운영 및 관리'),
            ('QA팀', 'qa-team', 'QA 및 테스트'),
            ('RA팀', 'ra-team', 'RA 업무'),
            ('N본부', 'n-division', 'N본부 전용'),
            ('E본부', 'e-division', 'E본부 전용'),
            ('보안팀', 'security', '보안 관련 시스템'),
            ('개발팀', 'dev-team', '개발 환경'),
        ]

        tenants = {}
        for name, slug, desc in tenant_data:
            tenant, _ = Tenant.objects.get_or_create(
                name=name,
                slug=slug,
                defaults={
                    'group': group,
                    'description': desc,
                    'comments': '[IDC-DUMMY]'
                }
            )
            tenants[slug] = tenant

        return tenants

    def create_manufacturers(self):
        """제조사 생성"""
        self.stdout.write('  제조사 생성 중...')

        mfr_data = [
            ('Dell', 'dell'),
            ('HP', 'hp'),
            ('Cisco', 'cisco'),
            ('Juniper', 'juniper'),
            ('Arista', 'arista'),
            ('Supermicro', 'supermicro'),
            ('Lenovo', 'lenovo'),
            ('IBM', 'ibm'),
            ('Netgear', 'netgear'),
            ('TP-Link', 'tp-link'),
        ]

        manufacturers = {}
        for name, slug in mfr_data:
            mfr, _ = Manufacturer.objects.get_or_create(
                name=name,
                slug=slug,
                defaults={'description': '[IDC-DUMMY]'}
            )
            manufacturers[slug] = mfr

        return manufacturers

    def create_device_types(self, manufacturers):
        """장비 유형 생성"""
        self.stdout.write('  장비 유형 생성 중...')

        device_type_data = [
            # 서버
            ('dell', 'PowerEdge R740', 'poweredge-r740', 2, True),
            ('dell', 'PowerEdge R640', 'poweredge-r640', 1, True),
            ('dell', 'PowerEdge R940', 'poweredge-r940', 4, True),
            ('hp', 'ProLiant DL380 Gen10', 'proliant-dl380-gen10', 2, True),
            ('hp', 'ProLiant DL360 Gen10', 'proliant-dl360-gen10', 1, True),
            ('supermicro', 'SuperServer 1029U', 'superserver-1029u', 1, True),
            ('lenovo', 'ThinkSystem SR650', 'thinksystem-sr650', 2, True),
            ('ibm', 'Power System S924', 'power-system-s924', 4, True),

            # 네트워크 장비
            ('cisco', 'Catalyst 9300', 'catalyst-9300', 1, True),
            ('cisco', 'Catalyst 9500', 'catalyst-9500', 1, True),
            ('cisco', 'Nexus 9300', 'nexus-9300', 1, True),
            ('cisco', 'ASR 1001-X', 'asr-1001-x', 1, True),
            ('juniper', 'EX4300', 'ex4300', 1, True),
            ('juniper', 'QFX5100', 'qfx5100', 1, True),
            ('arista', '7050X3', '7050x3', 1, True),

            # 공유기 (납품 장비 설정용)
            ('netgear', 'R7000', 'r7000', 1, False),
            ('tp-link', 'Archer AX6000', 'archer-ax6000', 1, False),
        ]

        device_types = {}
        for mfr_slug, model, slug, u_height, is_full_depth in device_type_data:
            dt, _ = DeviceType.objects.get_or_create(
                manufacturer=manufacturers[mfr_slug],
                model=model,
                slug=slug,
                defaults={
                    'u_height': u_height,
                    'is_full_depth': is_full_depth,
                    'comments': '[IDC-DUMMY]'
                }
            )
            device_types[slug] = dt

        return device_types

    def create_device_roles(self):
        """장비 역할 생성"""
        self.stdout.write('  장비 역할 생성 중...')

        role_data = [
            ('운영서버', 'ops-server', '0000ff', '운영 환경 서버'),
            ('테스트서버', 'test-server', '00ff00', '테스트 환경 서버'),
            ('개발서버', 'dev-server', 'ffff00', '개발 환경 서버'),
            ('DB서버', 'db-server', 'ff00ff', '데이터베이스 서버'),
            ('웹서버', 'web-server', '00ffff', '웹 애플리케이션 서버'),
            ('코어라우터', 'core-router', 'ff0000', '코어 네트워크 라우터'),
            ('백본스위치', 'backbone-switch', 'ff8000', '백본 네트워크 스위치'),
            ('액세스스위치', 'access-switch', 'ff8080', '액세스 레이어 스위치'),
            ('방화벽', 'firewall', '800000', '보안 방화벽'),
            ('납품장비', 'delivery-device', '808080', '납품 전 설정용 장비'),
            ('부서전용', 'dept-dedicated', 'c0c0c0', '부서 전용 장비'),
            ('미분류', 'unclassified', '404040', '미분류 장비'),
        ]

        roles = {}
        for name, slug, color, desc in role_data:
            role, _ = DeviceRole.objects.get_or_create(
                name=name,
                slug=slug,
                defaults={
                    'color': color,
                    'description': f'[IDC-DUMMY] {desc}'
                }
            )
            roles[slug] = role

        return roles

    def create_site(self):
        """사이트 생성"""
        self.stdout.write('  사이트 생성 중...')

        site, _ = Site.objects.get_or_create(
            name='본사 IDC',
            slug='hq-idc',
            defaults={
                'status': SiteStatusChoices.STATUS_ACTIVE,
                'facility': '본사 데이터센터',
                'physical_address': '서울특별시 강남구 테헤란로 123',
                'shipping_address': '서울특별시 강남구 테헤란로 123',
                'latitude': 37.5065,
                'longitude': 127.0536,
                'comments': '[IDC-DUMMY] IDC 운영 시뮬레이션용 사이트'
            }
        )

        return site

    def create_locations(self, site):
        """위치(서버실) 생성"""
        self.stdout.write('  위치(서버실) 생성 중...')

        location_data = [
            ('B1 서버실-일반구역', 'b1-general', 'B1층 일반 구역 서버실'),
            ('B1 서버실-보안구역', 'b1-secure', 'B1층 보안 구역 서버실'),
            ('3층 QA RA 서버실', '3f-qa-ra', '3층 QA/RA팀 서버실'),
            ('4층 N본부 서버실', '4f-n-div', '4층 N본부 전용 서버실'),
            ('5층 E본부 서버실', '5f-e-div', '5층 E본부 전용 서버실'),
        ]

        locations = {}
        for name, slug, desc in location_data:
            loc, _ = Location.objects.get_or_create(
                site=site,
                name=name,
                slug=slug,
                defaults={
                    'description': f'[IDC-DUMMY] {desc}'
                }
            )
            locations[slug] = loc

        return locations

    def create_racks(self, locations):
        """랙 생성"""
        self.stdout.write('  랙 생성 중...')

        # 각 서버실별 랙 수 (장비 수에 따라 조정)
        rack_config = {
            'b1-general': 4,    # 80대 -> 4개 랙
            'b1-secure': 8,     # 164대 -> 8개 랙
            '3f-qa-ra': 3,      # 54대 -> 3개 랙
            '4f-n-div': 6,      # 132대 -> 6개 랙
            '5f-e-div': 4,      # 67대 -> 4개 랙
        }

        racks = {}
        for loc_slug, rack_count in rack_config.items():
            location = locations[loc_slug]
            racks[loc_slug] = []

            for i in range(1, rack_count + 1):
                rack_name = f'{location.name}-RACK-{i:02d}'
                rack, _ = Rack.objects.get_or_create(
                    site=location.site,
                    location=location,
                    name=rack_name,
                    defaults={
                        'status': RackStatusChoices.STATUS_ACTIVE,
                        'u_height': 42,
                        'comments': '[IDC-DUMMY]'
                    }
                )
                racks[loc_slug].append(rack)

        return racks

    def create_vlans(self, site):
        """VLAN 생성"""
        self.stdout.write('  VLAN 생성 중...')

        vlan_group, _ = VLANGroup.objects.get_or_create(
            name='IDC VLAN',
            slug='idc-vlan',
            defaults={
                'scope_type': None,
                'description': '[IDC-DUMMY] IDC용 VLAN 그룹'
            }
        )

        vlan_data = [
            (10, 'Management', '관리 네트워크'),
            (20, 'Production', '운영 네트워크'),
            (30, 'Development', '개발 네트워크'),
            (40, 'Test', '테스트 네트워크'),
            (50, 'DMZ', 'DMZ 네트워크'),
            (100, 'Storage', '스토리지 네트워크'),
            (200, 'Backup', '백업 네트워크'),
        ]

        vlans = {}
        for vid, name, desc in vlan_data:
            vlan, _ = VLAN.objects.get_or_create(
                vid=vid,
                name=name,
                group=vlan_group,
                defaults={
                    'site': site,
                    'description': f'[IDC-DUMMY] {desc}'
                }
            )
            vlans[vid] = vlan

        return vlan_group

    def create_prefixes(self, site):
        """IP 대역 생성"""
        self.stdout.write('  IP 대역 생성 중...')

        prefix_data = [
            ('10.0.0.0/8', 'IDC 전체 대역'),
            ('10.1.0.0/16', 'B1 일반구역'),
            ('10.2.0.0/16', 'B1 보안구역'),
            ('10.3.0.0/16', '3층 QA RA'),
            ('10.4.0.0/16', '4층 N본부'),
            ('10.5.0.0/16', '5층 E본부'),
            ('192.168.0.0/16', '관리 네트워크'),
        ]

        prefixes = {}
        for prefix_str, desc in prefix_data:
            prefix, _ = Prefix.objects.get_or_create(
                prefix=prefix_str,
                defaults={
                    'site': site,
                    'description': f'[IDC-DUMMY] {desc}'
                }
            )
            prefixes[prefix_str] = prefix

        return prefixes

    def create_devices(self, locations, racks, device_types, device_roles, tenants):
        """장비 생성 - 현황에 맞게"""
        self.stdout.write('  장비 생성 중...')

        # 서버 유형 목록
        server_types = [
            'poweredge-r740', 'poweredge-r640', 'poweredge-r940',
            'proliant-dl380-gen10', 'proliant-dl360-gen10',
            'superserver-1029u', 'thinksystem-sr650', 'power-system-s924'
        ]

        # 네트워크 장비 유형
        network_types = [
            'catalyst-9300', 'catalyst-9500', 'nexus-9300',
            'asr-1001-x', 'ex4300', 'qfx5100', '7050x3'
        ]

        # 공유기 유형
        router_types = ['r7000', 'archer-ax6000']

        # 서버 역할
        server_roles = ['ops-server', 'test-server', 'dev-server', 'db-server', 'web-server']

        # 네트워크 역할
        network_roles = ['core-router', 'backbone-switch', 'access-switch', 'firewall']

        # 현황 데이터
        # (위치, 운영/테스트서버, 납품장비, 네트워크장비, 부서전용, 미분류)
        inventory = [
            ('b1-general', 48, 0, 12, 2, 18),
            ('b1-secure', 131, 0, 22, 3, 8),
            ('3f-qa-ra', 31, 0, 3, 8, 12),
            ('4f-n-div', 34, 9, 6, 18, 65),
            ('5f-e-div', 29, 9, 6, 5, 18),
        ]

        all_devices = []
        device_counter = 1

        for loc_slug, ops_count, delivery_count, network_count, dept_count, unclass_count in inventory:
            location = locations[loc_slug]
            loc_racks = racks[loc_slug]

            # 테넌트 매핑
            tenant_map = {
                'b1-general': tenants.get('infra-ops'),
                'b1-secure': tenants.get('security'),
                '3f-qa-ra': tenants.get('qa-team'),
                '4f-n-div': tenants.get('n-division'),
                '5f-e-div': tenants.get('e-division'),
            }
            default_tenant = tenant_map.get(loc_slug)

            # 1. 운영/테스트 서버 생성
            for i in range(ops_count):
                role = device_roles[random.choice(server_roles)]
                device_type = device_types[random.choice(server_types)]
                rack = random.choice(loc_racks)

                device = self._create_device(
                    name=f'SRV-{device_counter:04d}',
                    device_type=device_type,
                    role=role,
                    site=location.site,
                    location=location,
                    rack=rack,
                    tenant=default_tenant,
                    status=random.choice([
                        DeviceStatusChoices.STATUS_ACTIVE,
                        DeviceStatusChoices.STATUS_ACTIVE,
                        DeviceStatusChoices.STATUS_ACTIVE,
                        DeviceStatusChoices.STATUS_STAGED,
                        DeviceStatusChoices.STATUS_PLANNED,
                    ])
                )
                all_devices.append(device)
                device_counter += 1

            # 2. 납품 장비 (공유기)
            for i in range(delivery_count):
                device_type = device_types[random.choice(router_types)]
                rack = random.choice(loc_racks)

                device = self._create_device(
                    name=f'DLV-{device_counter:04d}',
                    device_type=device_type,
                    role=device_roles['delivery-device'],
                    site=location.site,
                    location=location,
                    rack=rack,
                    tenant=default_tenant,
                    status=DeviceStatusChoices.STATUS_INVENTORY
                )
                all_devices.append(device)
                device_counter += 1

            # 3. 네트워크 장비
            for i in range(network_count):
                device_type = device_types[random.choice(network_types)]
                role = device_roles[random.choice(network_roles)]
                rack = random.choice(loc_racks)

                device = self._create_device(
                    name=f'NET-{device_counter:04d}',
                    device_type=device_type,
                    role=role,
                    site=location.site,
                    location=location,
                    rack=rack,
                    tenant=default_tenant,
                    status=DeviceStatusChoices.STATUS_ACTIVE
                )
                all_devices.append(device)
                device_counter += 1

            # 4. 부서 전용 장비
            for i in range(dept_count):
                device_type = device_types[random.choice(server_types)]
                rack = random.choice(loc_racks)

                device = self._create_device(
                    name=f'DPT-{device_counter:04d}',
                    device_type=device_type,
                    role=device_roles['dept-dedicated'],
                    site=location.site,
                    location=location,
                    rack=rack,
                    tenant=default_tenant,
                    status=DeviceStatusChoices.STATUS_ACTIVE
                )
                all_devices.append(device)
                device_counter += 1

            # 5. 미분류 장비
            for i in range(unclass_count):
                device_type = device_types[random.choice(server_types + network_types)]
                rack = random.choice(loc_racks)

                device = self._create_device(
                    name=f'UNC-{device_counter:04d}',
                    device_type=device_type,
                    role=device_roles['unclassified'],
                    site=location.site,
                    location=location,
                    rack=rack,
                    tenant=None,
                    status=random.choice([
                        DeviceStatusChoices.STATUS_INVENTORY,
                        DeviceStatusChoices.STATUS_OFFLINE,
                        DeviceStatusChoices.STATUS_PLANNED,
                    ])
                )
                all_devices.append(device)
                device_counter += 1

        return all_devices

    def _create_device(self, name, device_type, role, site, location, rack, tenant, status):
        """개별 장비 생성"""
        device, created = Device.objects.get_or_create(
            name=name,
            defaults={
                'device_type': device_type,
                'role': role,
                'site': site,
                'location': location,
                'rack': rack,
                'tenant': tenant,
                'status': status,
                'serial': f'SN{random.randint(100000, 999999)}',
                'asset_tag': f'ASSET-{random.randint(10000, 99999)}',
                'comments': '[IDC-DUMMY]'
            }
        )

        if created:
            # 인터페이스 생성
            self._create_interfaces(device)

        return device

    def _create_interfaces(self, device):
        """장비에 인터페이스 생성"""
        # 관리 인터페이스
        Interface.objects.get_or_create(
            device=device,
            name='MGMT',
            defaults={
                'type': '1000base-t',
                'mgmt_only': True
            }
        )

        # 데이터 인터페이스 (2-4개)
        for i in range(random.randint(2, 4)):
            Interface.objects.get_or_create(
                device=device,
                name=f'eth{i}',
                defaults={
                    'type': random.choice(['1000base-t', '10gbase-t', '25gbase-x-sfp28'])
                }
            )

    def assign_ip_addresses(self, devices, prefixes):
        """장비에 IP 주소 할당"""
        self.stdout.write('  IP 주소 할당 중...')

        # 위치별 IP 대역 매핑
        ip_mapping = {
            'b1-general': '10.1',
            'b1-secure': '10.2',
            '3f-qa-ra': '10.3',
            '4f-n-div': '10.4',
            '5f-e-div': '10.5',
        }

        for device in devices:
            if not device.location:
                continue

            loc_slug = device.location.slug
            base_ip = ip_mapping.get(loc_slug, '10.0')

            # 관리 인터페이스에 IP 할당
            mgmt_interface = device.interfaces.filter(name='MGMT').first()
            if mgmt_interface:
                # 고유 IP 생성
                octet3 = random.randint(1, 254)
                octet4 = random.randint(1, 254)
                ip_addr = f'{base_ip}.{octet3}.{octet4}/24'

                ip, created = IPAddress.objects.get_or_create(
                    address=ip_addr,
                    defaults={
                        'assigned_object_type_id': Interface._meta.pk,
                        'assigned_object_id': mgmt_interface.pk,
                        'description': f'[IDC-DUMMY] {device.name} 관리 IP'
                    }
                )

                if created:
                    device.primary_ip4 = ip
                    device.save()
