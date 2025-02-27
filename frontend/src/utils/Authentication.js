export const isAuthenticated = () => {
    return localStorage.getItem('accessToken') !== null
}

export const getAccessToken = () => {
    return localStorage.getItem('accessToken')
}

export const getRefreshToken = () => {
    return localStorage.getItem('refreshToken')
}

export const getUserRole = () => {
    return localStorage.getItem('userRole')
}