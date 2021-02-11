import React, { useState } from 'react';
import './sass/Recover.scss';

const Recover = () => {
	const [mnemonics, updateMnemonics] = useState('');
	const [salt, updateSalt] = useState('');
	const [rootseed, updateRootseed] = useState('');

	const recover_seed = async () => {
		const resp = await fetch('/recover', {method: "POST", body: JSON.stringify({"mnemonics": mnemonics, "salt": salt})});
		const data = await resp.json();
		if (data && data["seed"])
			await updateRootseed(data["seed"]);
	}

	const update_seed = async (event) => {
		console.log(event.target.value);
		await updateMnemonics(event.target.value);
	}

	const update_salt = async (event) => {
		console.log(event.target.value);
		await updateSalt(event.target.value);
	}

	return (<><div id="recoveryinput">
			<input type="text" onChange={update_seed}/>
			<input type="text" onChange={update_salt}/>
			<button onClick={recover_seed}>Recover</button>
		</div><div id="recoveryseed">
			{rootseed}
		</div></>);
}

export {
	Recover
}
