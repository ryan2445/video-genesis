import Vue from 'vue'

export default () => {
  Vue.filter('userDisplayName', function (user) {
      if (user) {
        if (!!user.usersFirstName) {
            let name = user.usersFirstName

            if (!!user.usersLastName) {
                name = name.concat(' ', user.usersLastName)
            }

            return name
        }

        else if (!!user.usersLastName) {
            return user.usersLastName
        }

        if (!!user.username) {
            return user.username
        }
    }
    
    return 'Unknown User'
  })
}