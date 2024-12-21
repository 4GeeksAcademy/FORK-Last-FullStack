import React, { useContext } from "react";
import { Context } from "../store/appContext"
import { Link } from "react-router-dom";

export const Navbar = () => {

	const { actions, store } = useContext(Context)

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					{
						// TF?
						store.token ?
							<button
								className="btn btn-primary"
								onClick={() => actions.logout()}
							>Cerrar Sesión</button> :
							<>
								<button
									className="btn btn-primary me-3"
								>Login</button>

								<button
									className="btn btn-primary"
								>Register</button>
							</>
					}

				</div>
			</div>
		</nav>
	);
};