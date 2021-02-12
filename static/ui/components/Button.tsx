import * as React from 'react';
import './sass/Button.scss';

interface imagePath {
	icon: string;
};

export const Button = ({icon}:imagePath) => {
	return (<div className="button">
		<img className="buttonicon" src={icon}/>
	</div>);
}
