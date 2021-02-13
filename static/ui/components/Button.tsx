import * as React from 'react';
import './sass/Button.scss';

interface imagePath {
	icon: string;
	title: string;
};

export const Button = ({icon, title}:imagePath) => {
	return (<div className="button" title={title}>
		<img className="buttonicon" src={icon}/>
	</div>);
}
