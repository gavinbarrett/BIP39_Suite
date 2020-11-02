import React from 'react';
import './sass/Button.scss';

const Button = ({icon}) => {
	return (<div className="button">
		<img className="buttonicon" src={icon}/>
	</div>);
}

export {
	Button
}
