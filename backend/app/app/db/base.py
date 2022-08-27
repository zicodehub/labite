# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.client import Client  # noqa
from app.models.fournisseur import Fournisseur  # noqa
from app.models.depot import Depot  # noqa
from app.models.produit import Produit  # noqa
from app.models.produit import TypeProduit  # noqa
from app.models.commande import Commande  # noqa
