"""Repositories module."""
from typing import Callable, Iterator
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from .models import *
from app.common.exception import NotFoundError


class MlcRepository:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def find_by_id_with_infra(self, tenant_id: str, mlc_id: int) -> Mlc:
        with self.session_factory() as session:
            return session.execute(
                select(Mlc).options(
                    joinedload(Mlc.vip_list),
                    joinedload(Mlc.config),
                    joinedload(Mlc.infra_list)
                )
                    .where(Mlc.tenant_id == tenant_id)
                    .where(Mlc.id == mlc_id)
                    .where(Mlc.status != Status.DELETED)
                    .order_by(Mlc.id)
            ).columns(Mlc).unique().first()

    def find_all_with_infra(self, tenant_id: str) -> Iterator[Mlc]:
        with self.session_factory() as session:
            return session.execute(
                select(Mlc).options(
                    joinedload(Mlc.vip_list),
                    joinedload(Mlc.config),
                    joinedload(Mlc.infra_list)
                )
                    .where(Mlc.tenant_id == tenant_id)
                    .where(Mlc.status != Status.DELETED)
                    .order_by(Mlc.id)
            ).columns(Mlc).unique().all()

    def find_by_id_with_stack_id(self, tenant_id: str, stack_id, mlc_id: int):
        with self.session_factory() as session:
            return session.execute(
                select(Mlc).options(
                    joinedload(Mlc.vip_list),
                    joinedload(Mlc.config),
                    joinedload(Mlc.infra_list)
                )
                    .where(Mlc.id == mlc_id)
                    .where(Mlc.tenant_id == tenant_id)
                    .where(Mlc.stack_id == stack_id)
                    .where(Mlc.status != Status.DELETED)
                    .order_by(Mlc.id)
            ).columns(Mlc).first()

    def find_all_with_stack_id(self, tenant_id: str, stack_id) -> Iterator[Mlc]:
        with self.session_factory() as session:
            return session.execute(
                select(Mlc).options(
                    joinedload(Mlc.config)
                )
                    .where(Mlc.tenant_id == tenant_id)
                    .where(Mlc.status != Status.DELETED)
                    .where(Mlc.stack_id == stack_id)
                    .order_by(Mlc.id)
            ).columns(Mlc).unique().all()

    def find_by_id(self, tenant_id: str, mlc_id: int):
        with self.session_factory() as session:
            return session.execute(
                select(Mlc)
                    .where(Mlc.tenant_id == tenant_id)
                    .where(Mlc.id == mlc_id)
                    .where(Mlc.status != Status.DELETED)
            ).columns(Mlc).first()

    def find_all(self, tenant_id: str):
        with self.session_factory() as session:
            return session.execute(
                select(Mlc)
                    .where(Mlc.tenant_id == tenant_id)
                    .where(Mlc.status != Status.DELETED)
            ).columns(Mlc).all()

    def save(self, mlc: Mlc) -> str:
        with self.session_factory() as session:
            session.add(mlc)
            session.commit()
            session.refresh(mlc)
            return mlc.get_id()


    def update(self, mlc: Mlc):
        with self.session_factory() as session:
            session.add(mlc)
            session.commit()
            session.refresh(mlc)
            return mlc.get_id()

    
    def delete_by_id(self, tenant_id, mlc_id):
        with self.session_factory() as session:
            mlc = session.execute(
                select(Mlc)
                .where(tenant_id == tenant_id)
                .where(mlc_id == mlc_id)
            ).columns(Mlc).first()
            mlc.status = Status.DELETED
            session.commit()
            session.refresh()
            return mlc
