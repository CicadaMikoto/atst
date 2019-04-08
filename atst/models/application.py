from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from atst.models import Base
from atst.models.types import Id
from atst.models import mixins


class Application(Base, mixins.TimestampsMixin, mixins.AuditableMixin):
    __tablename__ = "applications"

    id = Id()
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    portfolio_id = Column(ForeignKey("portfolios.id"), nullable=False)
    portfolio = relationship("Portfolio")
    environments = relationship("Environment", back_populates="application")
    roles = relationship("ApplicationRole")

    @property
    def users(self):
        return set(role.user for role in self.roles)

    @property
    def num_users(self):
        return len(self.users)

    @property
    def displayname(self):
        return self.name

    def __repr__(self):  # pragma: no cover
        return "<Application(name='{}', description='{}', portfolio='{}', id='{}')>".format(
            self.name, self.description, self.portfolio.name, self.id
        )
