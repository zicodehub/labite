import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost/api/v1'
})

export const listClients = () => api.get('/clients/')
export const listFournisseurs = () => api.get('/fournisseurs/')
export const listTypesProduits = () => api.get('/types/')
export const listProduits = () => api.get('/produits/')
export const listDepots = () => api.get('/depots/')
export const listVehicules = () => api.get('/vehicules/')
export const listCommandes = () => api.get('/commandes/')


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
export const createTypeProduit = (data) => api.post(`/types`, data)
export const createDepot = (data) => api.post(`/depots`, data)

export const updateClient = (id, data) => api.put(`/clients/${id}`, data)
export const updateFournisseur = (id, data) => api.put(`/fournisseurs/${id}`, data)
export const updateDepot = (id, data) => api.put(`/depots/${id}`, data)

export const deleteCommande = (id) => api.delete(`/commandes/${id}`)
export const deleteClient = (id) => api.delete(`/clients/${id}`)
export const deleteDepot = (id) => api.delete(`/depots/${id}`)
export const deleteFournisseur = (id) => api.delete(`/fournisseurs/${id}`)
export const deleteVehicule = (id) => api.delete(`/vehicules/${id}`)

export const runGenetic = () => api.get(`/commandes/genetic`)

export const runRecuit = () => api.get(`/commandes/recuit`)


export const resetDB = () => api.get(`/commandes/reset-db`)
