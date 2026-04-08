import request from '../utils/request'

export const login = (data) => {
  return request({
    url: '/students/login',
    method: 'post',
    data
  })
}

export const register = (data) => {
  return request({
    url: '/students/register',
    method: 'post',
    data
  })
}

export const coachLogin = (data) => {
  return request({
    url: '/coaches/login',
    method: 'post',
    data
  })
}

export const coachRegister = (data) => {
  return request({
    url: '/coaches/register',
    method: 'post',
    data
  })
}

export const adminLogin = (data) => {
  return request({
    url: '/admins/login',
    method: 'post',
    data
  })
}