import * as React from 'react';
import './sass/PathSelector.scss';

export const PathSelector = () => {
	return (<div className="path-selector">
		<div className="address legacy">{"Legacy"}</div>
		<div className="address segwit">{"SegWit"}</div>
		<div className="address native-segwit">{"Native SegWit"}</div>
	</div>);
} 
