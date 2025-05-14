import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './components/Dashboard';
import './styles/global.css';

const App: React.FC = () => {
    return (
        <div className="App">
            <Header />
            <Dashboard />
            <Footer />
        </div>
    );
};

export default App;