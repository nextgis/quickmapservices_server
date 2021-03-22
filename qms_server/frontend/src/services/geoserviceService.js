const geoserviceService  = {
  async delete(id) {
    console.log('delete');
    try {
      const f = await fetch(`/api/v1/geoservices/delete/${id}`, { 
        method: 'delete',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
        }
      });
      const data = await f.json();
      if (data.status != 'ok') {
        const message = data.message || data.detail;
        throw new Error(`Error while deleting. API response: ${message}`);
      } else {
        window.location.href='/';
      }
      return data;
    } catch(error) {
      alert(error);
    }
  }
}

export default geoserviceService;