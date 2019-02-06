import React from 'react';
import axios from 'axios';

const LocationIndex = props => {
    const handleSearchSubmit = (e) => {
        if (e.keyCode === 13) {
            props.handleSearchLocation();
        }
    };

    const handleSearch = e => {
        let {locationSearch} = props;
        locationSearch.key = e.target.value;
        props.handleUpdateState({locationSearch});
    };

    const handleSelectLocation = key => {
        let {locationSearch} = props;
        let selectedLocationObj = locationSearch.results.facebook.find(function (element) {
            return element.key === key;
        });
        axios.post('/select-location', selectedLocationObj)
            .then(function (res) {
                if (res.data && res.data.added) {
                    locationSearch.results.local.push(selectedLocationObj);
                    props.handleUpdateState({locationSearch});
                    window.toastr.success(res.data.message)
                } else {
                    window.toastr.error(res.data.message)
                }

            });
    };

    return (
        <div className="row">
            <div className="col-md-12">
                <div className="row">
                    <div className="form-group">
                        <label>Search City or Country:</label><br/>
                        <input onChange={handleSearch} onKeyUp={handleSearchSubmit} type="text" className="form-control"
                               name="hint"/>

                    </div>
                </div>
                <div className="row">
                    <div className="col-md-6">
                        <h1>Result from Facebook</h1>
                        <ul id="fb-location-results">
                            {props.locationSearch.results.facebook && (
                                props.locationSearch.results.facebook.map(obj => (
                                    <li
                                        key={obj.key}
                                        onClick={() => handleSelectLocation(obj.key)}
                                        style={{cursor: 'pointer'}}
                                    >{`${obj.name}, ${obj.region ? obj.region + ',' : ''} ${obj.country_name}`}
                                    </li>
                                ))
                            )}
                        </ul>
                    </div>
                    <div className="col-md-6">
                        <h1>Result from Local DB</h1>
                        <ul id="fb-db-results">
                            {props.locationSearch.results.local && (
                                props.locationSearch.results.local.map((obj, index) => (
                                    <li
                                        key={index}
                                    >{`${obj.field_name ? obj.field_name : obj.name}, ${obj.region ? obj.region + ',' : ''} ${obj.country_name}`}
                                    </li>
                                ))
                            )}
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    );
};

export default LocationIndex;