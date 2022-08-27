from fastapi import APIRouter

from app.api.api_v1.endpoints import client, depot, fournisseur, type_produit, produit, commande, vehicule
api_router = APIRouter()
api_router.include_router(client.router, prefix="/clients")
api_router.include_router(fournisseur.router, prefix="/fournisseurs")
api_router.include_router(depot.router, prefix="/depots")
api_router.include_router(produit.router, prefix="/produits")
api_router.include_router(type_produit.router, prefix="/types")
api_router.include_router(commande.router, prefix="/commandes")
api_router.include_router(vehicule.router, prefix="/vehicules")
