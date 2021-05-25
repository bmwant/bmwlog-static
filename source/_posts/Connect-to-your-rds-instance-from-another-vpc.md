---
title: Connect to your RDS instance from another VPC
date: 2020-03-05 14:49:05
tags: [aws, rds, vpc, devops]
author: Misha Behersky
---

Suppose you have created a PostgreSQL database without public accessibility (we are talking about [AWS RDS](https://aws.amazon.com/rds/) right now) within some VPC (e.g. `VPC B`) and you have a regular EC2 instance in another VPC (e.g. `VPC A`). Now you want to connect a client (e.g. [psql](https://www.postgresql.org/docs/9.6/app-psql.html)) from an instance to database. VPC peering is a tool that you need to use in such a case

![vpc peering](/img/article/b09bcabcc27936b3ab95ae567b7a2276.png)

Check [different scenarios here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.Scenarios.html) if you want to connect from different VPC or without it altogether.

First of all you need to have a peering connection in place. Go to `Services` -> `VPC` -> `Peering Connections` and create new connection. Select *requester* (`VPC B`) and *accepter* (`VPC B`) and click *Create*. Then choose `Actions` -> `Accept Request` to activate created connection.

### Update route tables
Go to `Subnets` and check the subnet where you EC2 instance is launched. It should have route table associated with it.

![route table](/img/article/60c2372c1bf83e889ce4e0b22f57e32a.png)

Click on the target route table and choose `Actions` -> `Edit routes`.

![add route](/img/article/b7d95dd0bf083181b3d10ab7c463a579.png)

For the first VPC enter CIDR block of second VPC as a *Destination* and our *Target* is the peered connection we have already created. Do the same for the route tables of the second VPC. Now you have established routes between both of your VPCs.

You might have multiple subnets within the same VPC, so make sure to update all of them. Keep in mind that we are allowing resources to be accessed for the entire CIDR block because it's just a bit easier to setup but you can limit that to particular subnet/resources (check links in resources below) if you need to.

### Update security groups
Last thing is to actually allow incoming connections from your instance to a port database is listening on (in our case it's `5432`). Go to `RDS` -> `Databases` and click on your target database

![database sg](/img/article/58ca8979e135341ca7cc1c59678b7530.png)

Then select security group used and add a **private** IP address of your instance to the inbound rules like this

![update sg](/img/article/b899ad8d9f883889b6c3fd0053ea1fff.png)


### Final steps
Now you should be able to test connectivity to your database from an instance. Connect to it first

```bash
$ ssh ec2-user@<public-ip> -i ~/.ssh/your-key.pem
# e.g. ssh ec2-user@54.146.176.116 -i ~/.ssh/key.pem
```

and use either a [netcat utility](https://en.wikipedia.org/wiki/Netcat) to check if the connection is possible

```bash
$ nc -v mydb.abczdrihzcxr.us-east-1.rds.amazonaws.com 5432
```
or a regular client

```bash
$ psql postgres://user:password@mydb.abczdrihzcxr.us-east-1.rds.amazonaws.com:5432/database
```

That's it, database is available and ready to be used from an instance.

### Resources

* [AWS docs: create peering connection](https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html)
* [AWS docs: peering configuration for entire CIDR](https://docs.aws.amazon.com/vpc/latest/peering/peering-configurations-full-access.html#two-vpcs-full-access)