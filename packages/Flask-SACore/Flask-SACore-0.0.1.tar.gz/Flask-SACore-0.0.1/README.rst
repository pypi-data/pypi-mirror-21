====================================
Flask extension for SQLAlchemy Core.
====================================

To be used in projects that do not use the SQLAlchemy ORM, but only the core.

The idea is to start and end a transaction on request boundaries, the way
Pyramid is doing this with its Tweens.

