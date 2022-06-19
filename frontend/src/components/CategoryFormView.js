import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

const base_url = '/api/v0.1.0';

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      category: '',
    };
  }

  submitCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: `${base_url}/categories`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById('add-question-form').reset();
        return;
      },
      error: (error) => {
        alert('Unable to add category. Please try your request again');
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render () {
    return (
      <div id='add-form'>
        <h2>Add a New Category</h2>
        <form
          className='form-view'
          id='add-question-form'
          onSubmit={this.submitCategory}
        >
          <label>
            Category
            <input type='text' name='category' onChange={this.handleChange} />
          </label>
          <input type='submit' className='button' value='Submit' />
        </form>
      </div>
    );
  }
}

export default FormView;
