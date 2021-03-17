import * as React from 'react';
import * as Router from 'react-router-dom';

export const ScrollToTop = () => {
	const { pathname } = Router.useLocation();
	React.useEffect(() => {
		window.scrollTo(0, 0);
	}, [pathname]);
	return null;
}
