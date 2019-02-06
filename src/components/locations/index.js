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
         <React.Fragment>
            <div className="row">
                <div className="col-lg-12">
                    <div className="page-header">
                        <h1>Location Search</h1>
                    </div>
                    <div className="row">
                        <div className="col-lg-6">
                            <p>You can search from Country or City facebook and local</p>
                        </div>
                        <div className="col-lg-6">
                            <input onChange={handleSearch} value={props.locationSearch.key} onKeyUp={handleSearchSubmit} type="text" className="form-control"
                                   name="hint"/>
                        </div>
                    </div>

                </div>
            </div>
            <div className="row">
                <div className="col-lg-6">
                    <table className="table" id="table">
                        <thead>
                        <tr>
                            <th>Facebook Results</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.locationSearch.results.facebook && props.locationSearch.results.facebook.length > 0 ? (
                            props.locationSearch.results.facebook.map(obj => (
                                <tr
                                    key={obj.key}
                                    onClick={() => handleSelectLocation(obj.key)}
                                    style={{cursor: 'pointer'}}
                                >
                                    <td>{`${obj.name}, ${obj.region ? obj.region + ',' : ''} ${obj.country_name}`}</td>
                                </tr>
                            ))
                        ) : (
                            <tr><td>No Results</td></tr>
                        )}
                        </tbody>
                    </table>
                    <hr/>
                </div>

                <div className="col-lg-6">
                    <table className="table" id="table">
                        <thead>
                        <tr>
                            <th>Local Results</th>
                        </tr>
                        </thead>
                        <tbody>
                        {props.locationSearch.results.local && props.locationSearch.results.local.length > 0 ? (
                            props.locationSearch.results.local.map((obj, index) => (
                                <tr
                                    key={index}
                                ><td>{`${obj.field_name ? obj.field_name : obj.name}, ${obj.region ? obj.region + ',' : ''} ${obj.country_name}`}</td>
                                </tr>
                            ))
                        ): (
                            <tr><td>No Results</td></tr>
                        )}
                        </tbody>
                    </table>
                    <hr/>
                </div>

            </div>
        </React.Fragment>
    );
};

export default LocationIndex;
