from dataclasses import dataclass
from core.shared.models import Email, AppBaseException
from core.shared.ports import ResponsePort, EmailRepositoryPort, PlanetRepositoryPort
from pydantic import BaseModel


class EmailNotFoundException(AppBaseException):
    msg = "Email not found"


class PlanetSendEmailRequest(BaseModel):
    planet_id_receiver: str
    title: str
    sub_title: str
    template: str
    body: str
    sender: str = "Universe"


@dataclass
class PlanetEmails:
    planet_repository_port: PlanetRepositoryPort
    email_repository_port: EmailRepositoryPort
    response_port: ResponsePort

    async def create(self, email_request: PlanetSendEmailRequest):
        planet = await self.planet_repository_port.get(email_request.planet_id_receiver)
        email = Email(title=email_request.title,
                      sub_title=email_request.sub_title,
                      template=email_request.template,
                      body=email_request.body,
                      sender=email_request.sender,
                      read=False,
                      planet=email_request.planet_id_receiver)

        email = await self.email_repository_port.create(email)
        planet.emails.append(email)
        await self.planet_repository_port.update(planet)

        return await self.response_port.publish_response(email)

    async def mark_as_read(self, email_id: str):
        email: Email = await self.email_repository_port.get(email_id)

        if email is None:
            raise EmailNotFoundException()

        email.read = True
        await self.email_repository_port.update(email)
        return await self.response_port.publish_response({})

    async def delete(self, email_id: str):
        email: Email = await self.email_repository_port.get(email_id)

        if email is None:
            raise EmailNotFoundException()

        await self.email_repository_port.delete(email)
        return await self.response_port.publish_response({})

