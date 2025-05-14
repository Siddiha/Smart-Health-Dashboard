import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer>
            <div className="footer-content">
                <p>&copy; {new Date().getFullYear()} Smart Health Dashboard. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;