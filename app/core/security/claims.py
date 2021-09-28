from typing import List, Dict, Optional
from datetime import datetime
import simplejson as json


class Claims(object):
    def __init__(self, content: Dict) -> None:
        self.__content = content

    @staticmethod
    def parse(content: str):
        content_map: Dict = json.loads(content)
        return Claims(content=content_map)

    def subject(self) -> Optional[str]:
        return self.__content['sub'] if 'sub' in self.__content else None

    def audience(self) -> Optional[str]:
        return self.__content['aud'] if 'aud' in self.__content else None

    def id(self) -> Optional[str]:
        return self.__content['jti'] if 'jti' in self.__content else None

    def vendor_identifier(self) -> Optional[str]:
        return self.__content['vdi'] if 'vdi' in self.__content else None

    def roles(self) -> List[str]:
        return self.__content['roles'] if 'roles' in self.__content else []

    def permissions(self) -> List[str]:
        return self.__content['permissions'] if 'permissions' in self.__content else []

    def expiry(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.__content['exp']) if 'exp' in self.__content else None

    def not_before(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.__content['nbf']) if 'nbf' in self.__content else None

    def issued_at(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.__content['iat']) if 'iat' in self.__content else None

    def has_roles(self, roles: List[str]) -> bool:
        contained_roles = self.roles()
        if contained_roles is None:
            return False
        for contained_role in contained_roles:
            if contained_role in roles:
                return True
        return False

    def has_permissions(self, permissions: List[str]) -> bool:
        contained_permissions = self.permissions()
        if contained_permissions is None:
            return False
        for contained_permission in contained_permissions:
            if contained_permission in permissions:
                return True
        return False
