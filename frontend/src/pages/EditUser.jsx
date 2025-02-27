import React from 'react'
import Header from '../components/Header'
import classes from './EditUser.module.css'

function EditUserPage() {
  return (
    <div className={classes.container}>
      <Header title={'Edit User'}/>
    </div>
  )
}

export default EditUserPage