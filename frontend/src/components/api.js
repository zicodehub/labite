import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8888/api/v1'
})

export const listClients = () => api.get('/clients')
export const listFournisseurs = () => api.get('/fournisseurs')
export const listTypesProduits = () => api.get('/types')
export const listProduits = () => api.get('/produits')
export const listDepots = () => api.get('/depots')
export const listVehicules = () => api.get('/vehicules')
export const listCommandes = () => api.get('/commandes')


export const getClient = (id) => api.get(`/clients/${id}`)
export const getFournisseur = (id) => api.get(`/fournisseurs/${id}`)
export const getProduit = (id) => api.get(`/produits/${id}`)
export const getDepot = (id) => api.get(`/depots/${id}`)
export const getCommande = (id) => api.get(`/commandes/${id}`)

export const createClient = (data) => api.post(`/clients`, data)
export const createFournisseur = (data) => api.post(`/fournisseurs`, data)
export const createCommande = (data) => api.post(`/commandes`, data)
export const createProduit = (data) => api.post(`/produits`, data)
export const createVehicule = (data) => api.post(`/vehicules`, data)

export const runGenetic = () => api.get(`/commandes/genetic`)

export const runRecuit = () => api.get(`/commandes/recuit`)