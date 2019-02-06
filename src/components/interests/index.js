import React from 'react';
import axios from 'axios';

const InterestIndex = props => {
    const handleSearchSubmit = (e) => {
        if (e.keyCode === 13) {
            props.handleSearchInterest();
        }
    };

    const handleSearch = e => {
        let {interestSearch} = props;
        interestSearch.key = e.target.value;
        props.handleUpdateState({interestSearch});
    };

    const handleSelectInterest = key => {
        let {interestSearch} = props;
        let selectedInterestObj = interestSearch.results.facebook.find(function (element) {
            return element.id === key;
        });
        axios.post('/select-interest', selectedInterestObj)
            .then(function (res) {
                if (res.data && res.data.added) {
                    interestSearch.results.local.push(selectedInterestObj);
                    props.handleUpdateState({interestSearch});
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
                        <h1>Interest Search</h1>
                    </div>
                    <div className="row">
                        <div className="col-lg-6">
                            <p>You can search from facebook and local</p>
                        </div>
                        <div className="col-lg-6">
                            <input onChange={handleSearch} onKeyUp={handleSearchSubmit} type="text" className="form-control"
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
                        {props.interestSearch.results.facebook && props.interestSearch.results.facebook.length > 0 ? (
                            props.interestSearch.results.facebook.map(obj => (
                                <tr
                                    key={obj.id}
                                    onClick={() => handleSelectInterest(obj.id)}
                                    style={{cursor: 'pointer'}}
                                >
                                    <td>{`${obj.name}, ${obj.audience_size}`}</td>
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
                        {props.interestSearch.results.local && props.interestSearch.results.local.length > 0 ? (
                            props.interestSearch.results.local.map((obj, index) => (
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

export default InterestIndex;
