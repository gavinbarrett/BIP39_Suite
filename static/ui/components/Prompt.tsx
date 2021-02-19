import * as React from 'react';
import './sass/Prompt.scss';

type PromptText = {
	texts: string[];
};

export const Prompt = ({texts}:PromptText) => {
	return (<div className="prompt">
		<div className="prompt-box">
		{texts.map((text, id) => {
			return <div className="prompt-line">{`${id + 1}. ${text}`}</div>
		})}
		</div>
	</div>);
}
