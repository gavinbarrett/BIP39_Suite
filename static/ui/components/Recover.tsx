import * as React from 'react';
import { SeedContainer } from './SeedContainer';
import './sass/Recover.scss';

export const Recover = () => {
	const [mnemonics, updateMnemonics] = React.useState('');
	const [salt, updateSalt] = React.useState('');
	const [rootseed, updateRootseed] = React.useState('');
	const [xprv, updateXprv] = React.useState('');
	const [xpub, updateXpub] = React.useState('');

	const recover_seed = async () => {
		const resp = await fetch('/recover', {method: "POST", body: JSON.stringify({"mnemonics": mnemonics, "salt": salt})});
		const data = await resp.json();
		if (data && data["seed"]) {
			console.log(Object.getOwnPropertyNames(data));
			updateRootseed(data["seed"]);
			updateXprv(data["m_xprv"]);
			updateXpub(data["m_xpub"]);
		}
	}
	const update_seed = event => {
		updateMnemonics(event.target.value);
	}
	const update_salt = event => {
		updateSalt(event.target.value);
	}
	return (<div className="recovery-box">
	<div className="recovery-input">
			<input type="text" className="" placeholder="Enter mnemonic seed phrase here" title="Mnemonic Seed" onChange={update_seed}/>
			<input type="text" className="" placeholder="Enter passphrase here" title="Salting Phrase" onChange={update_salt}/>
			<button className="recovery-button" onClick={recover_seed}>Recover</button>
		</div><div className="recovery-seed">
			{rootseed ? <SeedContainer phrase={mnemonics} seed={rootseed} m_xprv={xprv} m_xpub={xpub}/> : ""}
		</div>
	</div>);
}
