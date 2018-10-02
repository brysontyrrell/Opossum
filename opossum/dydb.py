import boto3


_dynamodb = boto3.resource('dynamodb')


def scan_table(table_name):
    table = _dynamodb.Table(table_name)

    results = table.scan()
    while True:
        for row in results['Items']:
            yield row
        if results.get('LastEvaluatedKey'):
            results = dynamodb.scan(
                ExclusiveStartKey=results['LastEvaluatedKey'])
        else:
            break
