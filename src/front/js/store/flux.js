
const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token : localStorage.getItem("token") || null,
			currentUser : localStorage.getItem("userCurrent") || null
			
		},
		actions: {
			register : async (user) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/register`, {
						method : "POST",
						headers : {
							"Content-Type" : "application/json"
						},
						body : JSON.stringify(user)
					})
					return response.status
					
				} catch (error) {
					console.log(error);
					// WARNING
				
					
					
				}
			},
			login : async(user) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/login`, {
						method : "POST",
						headers : {
							"Content-Type" : "application/json"
						},
							body : JSON.stringify(user)
						
					})

					const data = await response.json()
					if (response.ok) {
						setStore({
							token : data.token,
							currentUser : data.current_user
						})

						localStorage.setItem("token", data.token)
						localStorage.setItem("currentUser", JSON.stringify(data.current_user))

					}
					return response.status
					
					
					console.log(data);
				} catch (error) {
					console.log(error);
					return false
					
					
				}
			},
			logout : () => {
				setStore({
					token : null,
					currentUser : null
				})
				localStorage.removeItem("token")
				localStorage.removeItem("currentUser")

				
			}
		}
	};
};

export default getState;
