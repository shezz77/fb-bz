import React, {Component} from 'react';
import LocationSearch from './components/locations/index';
import InterestSearch from './components/interests/index';
import axios from 'axios';

class App extends Component {
    state = {
        locationSearch: {
            key: '',
            results: {
                facebook: [],
                local: []
            }
        },
        interestSearch: {
            key: '',
            results: {
                facebook: [],
                local: []
            }
        }
    };

    handleUpdateState = (ObjectToChange) => this.setState({...ObjectToChange});

    handleSearchLocation = () => {
        if (this.state.locationSearch.key) {
            axios.get(`/search-city?q=${this.state.locationSearch.key}`)
                .then(res => {
                    if (res.data) {
                        let {locationSearch} = this.state;
                        if (res.data.facebook && res.data.facebook.data) {
                            locationSearch.results.facebook = res.data.facebook.data
                        }
                        if (res.data.local) {
                            locationSearch.results.local = res.data.local
                        }
                        this.setState({locationSearch})
                    }
                })
        }
    };

      handleSearchInterest = () => {
        if (this.state.interestSearch.key) {
            axios.get(`/search-interest?q=${this.state.interestSearch.key}`)
                .then(res => {
                    console.log(res);
                    if (res.data) {
                        let {interestSearch} = this.state;
                        if (res.data.facebook && res.data.facebook.data) {
                            interestSearch.results.facebook = res.data.facebook.data
                        }
                        if (res.data.local) {
                            interestSearch.results.local = res.data.local
                        }
                        this.setState({interestSearch})
                    }
                })
        }
    };

    render() {
        return (
            <div>
                <LocationSearch
                    {...this.state}
                    handleUpdateState={this.handleUpdateState}
                    handleSearchLocation={this.handleSearchLocation}
                />
                <InterestSearch
                    {...this.state}
                    handleUpdateState={this.handleUpdateState}
                    handleSearchInterest={this.handleSearchInterest}
                />
            </div>
        );
    }
}

export default App;
