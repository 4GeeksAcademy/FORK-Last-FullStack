import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import Todos from "./Todos.jsx";
import { Navigate } from "react-router-dom";
import Login from "./Login.jsx";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<>
		{
			store.token ?
			<Todos/> :
			<Navigate to={"/login"}/>
		}
		</>
	);
	
};
