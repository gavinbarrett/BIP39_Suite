import * as React from 'react';
import './sass/PathSelector.scss';

interface pathSelector {
	path: string;
	updatePath: (string) => string;
};

interface pathType {
	style: string;
	type: string;
	path: string;
	updatePath: (string) => string;
};

const Path = ({style, type, path, updatePath}:pathType) => {
	const ptype = (type === path) ? 'active' : '';
	const changePath = () => {
		updatePath(type)
	}
	return (<div className={`${style} ${ptype}`} onClick={changePath}>{type}</div>);
}

export const PathSelector = ({path, updatePath}:pathSelector) => {
	return (<div className="path-selector">
		<Path style={"address legacy"} type={"Legacy"} path={path} updatePath={updatePath}/>
		<Path style={"address segwit"} type={"SegWit"} path={path} updatePath={updatePath}/>
		<Path style={"address native-segwit"} type={"Native SegWit"} path={path} updatePath={updatePath}/>
	</div>);
} 
