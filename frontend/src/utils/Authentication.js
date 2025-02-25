export const isAuthenticated = () => {
    return localStorage.getItem('accessToken') !== null
}

export const getUserRole = () => {
    return localStorage.getItem('role')
}