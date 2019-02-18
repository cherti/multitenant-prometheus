Vagrant.configure("2") do |config|

  config.vm.box = "generic/debian9"
  config.vm.network "forwarded_port", guest: "443", host: "8000"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "multitenant-prometheus.yml"
	ansible.force_remote_user = false
	ansible.extra_vars = { ansible_ssh_user: 'vagrant', ansible_password: 'vagrant' }
    ansible.sudo = true
    #ansible.verbose = 'vvvv'
  end

end
