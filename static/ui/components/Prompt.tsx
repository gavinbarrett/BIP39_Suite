import * as React from 'react';
import './sass/Prompt.scss';

type PromptText = {
	text: string;
};

export const Prompt = ({text}:PromptText) => {
	return (<div className="prompt">
		{text}
	</div>);
}
